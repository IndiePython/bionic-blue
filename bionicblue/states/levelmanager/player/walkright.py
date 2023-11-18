
### third-party imports

from pygame.locals import (

    QUIT,
    K_a, K_d,
    K_w,

    KEYDOWN,
    KEYUP,
    K_ESCAPE,
    K_j, K_k
)


### local imports

from ....config import PROJECTILES, quit_game

from ....constants import (
    MAX_X_SPEED,
    SHOOTING_STANCE_FRAMES,
    DAMAGE_REBOUND_FRAMES,
)

from ....pygamesetup import SERVICES_NS

from ....pygamesetup.constants import GENERAL_NS

from .projectiles.default import DefaultProjectile
from .projectiles.chargedshot import ChargedShot



class WalkRight:

    def walk_right_control(self):

        ###

        for event in SERVICES_NS.get_events():

            if event.type == QUIT:
                quit_game()

            elif event.type == KEYDOWN:

                if event.key == K_ESCAPE:
                    quit_game()

                elif event.key == K_j:
                    self.walk_right_shoot()

                elif event.key == K_k:
                    self.jump()

                elif event.key == K_w:

                    self.check_ladder()

                    if self.ladder:

                        self.set_state('idle_right')
                        self.aniplayer.switch_animation('climbing')

                        return

            elif event.type == KEYUP:

                if event.key == K_j and self.charge_start:

                    result = self.stop_charging()

                    if result:
                        self.walk_right_release_charge(result)

        ###

        pressed_state = SERVICES_NS.get_pressed_keys()

        if pressed_state[K_a]:

            self.x_accel += -1

            if self.aniplayer.anim_name == 'shooting_walk_right':
                self.set_state('decelerate_right')
                self.aniplayer.switch_animation('decelerate_right')
                self.aniplayer.blend('+shooting')

            else:
                self.set_state('decelerate_right')
                self.aniplayer.switch_animation('decelerate_right')

        elif pressed_state[K_d]:
            self.x_accel = min(self.x_accel + 1, 2)

        else:
            self.x_accel = max(self.x_accel - 1, 0)

    def walk_right_update(self):

        x = self.rect.x

        if self.x_speed > 0:
            self.x_speed += -1

        self.x_speed += self.x_accel
        self.x_speed = min(max(self.x_speed, 0), MAX_X_SPEED)

        self.rect.x += self.x_speed

        if not self.x_speed:
            self.set_state('idle_right')
            self.aniplayer.switch_animation('idle_right')

        current_frame = GENERAL_NS.frame_index

        if current_frame - self.last_shot >= SHOOTING_STANCE_FRAMES:
            self.aniplayer.blend('-shooting')

        if self.charge_start:
            self.check_charge()

        if self.rect.x != x:
            self.avoid_blocks_horizontally()

        self.react_to_gravity()

        if current_frame - self.last_damage > DAMAGE_REBOUND_FRAMES:
            self.check_invisibility()

    def walk_right_shoot(self):

        pos_value = self.rect.move(2, -2).midright

        PROJECTILES.add(
            DefaultProjectile(
                x_orientation=1,
                pos_name='center',
                pos_value=pos_value,
            )
        )

        self.aniplayer.blend('+shooting')
        self.charge_start = self.last_shot = GENERAL_NS.frame_index

    def walk_right_release_charge(self, charge_type):

        pos_value = self.rect.move(10, -2).midright

        PROJECTILES.add(
            ChargedShot(
                charge_type,
                x_orientation=1,
                pos_name='center',
                pos_value=pos_value,
            )
        )

        self.aniplayer.blend('+shooting')

        self.last_shot = GENERAL_NS.frame_index
