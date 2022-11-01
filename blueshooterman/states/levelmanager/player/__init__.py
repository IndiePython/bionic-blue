
### third-party import
from pygame.time import get_ticks as get_msecs


### local imports

from ....config import (
    SOUND_MAP,
    GRAVITY_ACCEL,
    MAX_Y_SPEED,
    BLOCKS_ON_SCREEN,
    DAMAGE_REBOUND_MSECS,
)

from ....pygameconstants import SCREEN_RECT

from ....ani2d.player import AnimationPlayer2D


## states

from .teleportingin import TeleportingIn

from .idleright import IdleRight
from .idleleft import IdleLeft

from .walkright import WalkRight
from .walkleft import WalkLeft

from .decelerateright import DecelerateRight
from .decelerateleft import DecelerateLeft

from .hurt import Hurt


class Player(
    TeleportingIn,
    IdleRight,
    IdleLeft,
    WalkRight,
    WalkLeft,
    DecelerateRight,
    DecelerateLeft,
    Hurt,
):

    def __init__(self):

        self.health = 32

        self.midair = False

        self.aniplayer = (
            AnimationPlayer2D(
                self, 'blue_shooter_man', 'teleporting', 'center', (SCREEN_RECT.centerx, -122)
            )
        )


        ###

        self.last_shot = 0
        self.last_damage = 0

        ###

        self.x_speed = 0
        self.y_speed = MAX_Y_SPEED
        self.x_accel = 0
        self.y_accel = 10

        self.jump_dy = -15

        ###
        self.set_state('teleporting_in')

    def prepare(self):

        self.rect.center = SCREEN_RECT.center
        self.y_speed = MAX_Y_SPEED
        self.aniplayer.switch_animation('teleporting')
        self.set_state('teleporting_in')

    def set_state(self, state_name):

        self.state_name = state_name

        for general_name, specific_name in (
            ('control', 'control'),
            ('update', 'state_update'),
        ):

            method = getattr(self, f'{state_name}_{general_name}')
            setattr(self, specific_name, method)

        if state_name in self.aniplayer.anim_names:
            self.aniplayer.switch_animation(state_name)

    def update(self):

        x = self.rect.x

        self.state_update()

        if self.rect.x != x:
            self.avoid_blocks_horizontally()

        self.react_to_gravity()

        if get_msecs() - self.last_damage > DAMAGE_REBOUND_MSECS:
            self.aniplayer.restore_constant_drawing()

    def draw(self):
        self.aniplayer.draw()

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

        now = get_msecs()

        if now - self.last_damage <= DAMAGE_REBOUND_MSECS:
            return

        ap = self.aniplayer

        self.health += -amount
        SOUND_MAP['blue_shooter_man_hurt.wav'].play()

        if self.health <= 0:
            print('died')

        new_anim = 'hurt_right' if ap.anim_name.endswith('right') else 'hurt_left'
        ap.switch_animation(new_anim)

        self.y_speed = -5

        if new_anim == 'hurt_right':
            self.x_speed = -1

        else:
            self.x_speed = 1

        self.set_state('hurt')
        self.last_damage = now
        ap.start_intermittent_drawing()
