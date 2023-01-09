
### standard library import
from itertools import chain


### local imports

from ....config import (
    REFS,
    SOUND_MAP,
    GRAVITY_ACCEL,
    MAX_Y_SPEED,
    BLOCKS_ON_SCREEN,
    DAMAGE_REBOUND_MSECS,
    MIDDLE_CHARGE_MSECS,
    FULL_CHARGE_MSECS,
)

from ....pygameconstants import SCREEN_RECT, blit_on_screen, SCREEN

from ....ourstdlibs.behaviour import do_nothing

## classes for composition

from ....ani2d.player import AnimationPlayer2D

from .healthcolumn import HealthColumn


## states

from .teleportingin import TeleportingIn

from .idleright import IdleRight
from .idleleft import IdleLeft

from .walkright import WalkRight
from .walkleft import WalkLeft

from .decelerateright import DecelerateRight
from .decelerateleft import DecelerateLeft

from .hurt import Hurt
from .dead import Dead


class Player(
    TeleportingIn,
    IdleRight,
    IdleLeft,
    WalkRight,
    WalkLeft,
    DecelerateRight,
    DecelerateLeft,
    Hurt,
    Dead,
):

    def __init__(self):

        self.midair = False

        self.death_rings_aniplayer = (
            AnimationPlayer2D(self, 'death_rings', 'expanding')
        )

        self.blue_shooter_man_aniplayer = (
            AnimationPlayer2D(
                self, 'blue_shooter_man', 'teleporting', 'center', (SCREEN_RECT.centerx, -122)
            )
        )

        ###
        self.draw_charge_fx = do_nothing

        ###

        self.last_shot = self.last_damage = self.charge_start = 0

        ###

        self.x_speed = 0
        self.y_speed = MAX_Y_SPEED
        self.x_accel = 0
        self.y_accel = 10

        self.jump_dy = -15

    def prepare(self):

        if not hasattr(self, 'health_column'):
            self.health_column = HealthColumn()

        self.rect.center = (SCREEN_RECT.centerx, -122)
        self.y_speed = MAX_Y_SPEED

        self.aniplayer = self.blue_shooter_man_aniplayer
        self.rect = self.aniplayer.root.rect

        self.aniplayer.switch_animation('teleporting')
        self.set_state('teleporting_in')

    def set_state(self, state_name):

        self.state_name = state_name

        for operation_name in ('control', 'update'):

            method = getattr(self, f'{state_name}_{operation_name}')
            setattr(self, operation_name, method)

        if state_name in self.aniplayer.anim_names:
            self.aniplayer.switch_animation(state_name)

    def draw(self):
        self.draw_charge_fx()
        self.aniplayer.draw()

    def draw_middle_charge_fx(self):
        """Draw particles to indicate middle charge."""
        ...

    def draw_full_charge_fx(self):
        """Draw particles to indicate full charge."""
        ...

    def avoid_blocks_horizontally(self):

        rect = self.rect

        for block in BLOCKS_ON_SCREEN:

            if block.colliderect(rect):

                if rect.left < block.rect.left:
                    rect.right = block.rect.left

                else:
                    rect.left = block.rect.right

                x_speed = 0

                break

    def react_to_gravity(self):

        ### react_to_blocks on y axis

        rect = self.rect

        y_speed = self.y_speed

        y_speed = min(y_speed + GRAVITY_ACCEL, MAX_Y_SPEED)

        rect.y += y_speed

        self.midair = True

        for block in BLOCKS_ON_SCREEN:

            if block.colliderect(rect):

                if rect.bottom < block.rect.bottom:

                    rect.bottom = block.rect.top
                    self.midair = False

                else:
                    rect.top = block.rect.bottom

                y_speed = 0

                break

        self.y_speed = y_speed

        ###

        ap = self.aniplayer
        anim_name = ap.anim_name

        orient = 'right' if anim_name.endswith('right') else 'left'

        if self.midair:

            if anim_name in {'teleporting', 'hurt_right', 'hurt_left'}: return

            blend_shooting = 'shooting' in anim_name

            if orient == 'right':
                ap.ensure_animation('jump_right')

            else:
                ap.ensure_animation('jump_left')

            if blend_shooting: ap.blend('+shooting')

        else:

            if 'jump' in anim_name:

                if self.x_speed > 0: anim_name = 'walk'
                elif self.x_speed < 0: anim_name = 'walk'
                else: anim_name = 'idle'

                ap.ensure_animation(f'{anim_name}_{orient}')

            else:
                ap.blend('+grounded')

    def jump(self):

        if not self.midair:
            self.y_speed += self.jump_dy
            SOUND_MAP['blue_shooter_man_jump.wav'].play()

    def damage(self, amount):
        if self.state_name == 'dead': return

        now = REFS.msecs

        if now - self.last_damage <= DAMAGE_REBOUND_MSECS:
            return

        ap = self.aniplayer

        self.health_column.damage(amount)

        if self.health_column.is_depleted():

            self.die()
            return

        else: SOUND_MAP['blue_shooter_man_hurt.wav'].play()

        new_anim = 'hurt_right' if ap.anim_name.endswith('right') else 'hurt_left'
        ap.switch_animation(new_anim)

        self.y_speed = -5

        if new_anim == 'hurt_right':
            self.x_speed = -1

        else:
            self.x_speed = 1

        self.set_state('hurt')
        self.last_damage = now

        ap.set_custom_surface_cycling(

            list(

                chain.from_iterable(

                    ('invisible', item)
                    for item in ap.cycle_values

                )

            )

        )

    def check_invisibility(self):

        if 'invisible' in self.aniplayer.cycle_values:

            l = list(self.aniplayer.cycle_values)

            while 'invisible' in l:
                l.remove('invisible')

            self.aniplayer.set_custom_surface_cycling(l)

    def check_charge(self):

        diff = REFS.msecs - self.charge_start

        if diff >= FULL_CHARGE_MSECS:

            if self.draw_charge_fx != self.draw_full_charge_fx:

                self.aniplayer.set_custom_surface_cycling(
                    ('caustic_blue', 'invisible', 'caustic_green', 'invisible')
                    if 'invisible' in self.aniplayer.cycle_values
                    else ('caustic_blue', 'caustic_green', 'caustic_blue')
                )

                self.draw_charge_fx = self.draw_full_charge_fx
                SOUND_MAP['blue_shooter_man_full_charge.wav'].play(-1)

        elif diff >= MIDDLE_CHARGE_MSECS:

            if self.draw_charge_fx != self.draw_middle_charge_fx:

                self.aniplayer.set_custom_surface_cycling(
                    ('default', 'invisible', 'caustic_blue', 'invisible', 'default')
                    if 'invisible' in self.aniplayer.cycle_values
                    else ('default', 'caustic_blue', 'default')
                )

                self.draw_charge_fx = self.draw_middle_charge_fx
                SOUND_MAP['blue_shooter_man_middle_charge.wav'].play()


    def stop_charging(self):

        msecs = REFS.msecs

        diff = msecs - self.charge_start

        if 'invisible' in self.aniplayer.cycle_values:

            self.aniplayer.set_custom_surface_cycling(
                ('invisible', 'default')
            )

        else:
            self.aniplayer.restore_surface_cycling()

        self.charge_start = 0
        SOUND_MAP['blue_shooter_man_full_charge.wav'].stop()
        SOUND_MAP['blue_shooter_man_middle_charge.wav'].stop()
        self.draw_charge_fx = do_nothing

        if diff >= FULL_CHARGE_MSECS:
            return 'full'

        elif diff >= MIDDLE_CHARGE_MSECS:
            return 'middle'

    def die(self):

        self.stop_charging()
        self.set_state('dead')
        self.aniplayer = self.death_rings_aniplayer

        center = self.rect.center
        self.rect = self.aniplayer.root.rect
        self.rect.center = center

        REFS.disable_player_tracking()
        SOUND_MAP['blue_shooter_man_death.wav'].play()
