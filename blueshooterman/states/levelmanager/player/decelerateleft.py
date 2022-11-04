
### third-party imports

from pygame import quit as quit_pygame

from pygame.locals import (

    QUIT,
    K_a, K_d,

    KEYDOWN,
    K_ESCAPE,
    K_j, K_k,

)

from pygame.color import THECOLORS

from pygame.event import get as get_events

from pygame.key import get_pressed as get_pressed_state

from pygame.time import get_ticks as get_msecs


### local imports

from ....config import PROJECTILES, DAMAGE_REBOUND_MSECS

from .projectiles.default import DefaultProjectile



class DecelerateLeft:

    def decelerate_left_control(self):

        ###

        for event in get_events():

            if event.type == QUIT:
                quit_pygame()
                quit()

            elif event.type == KEYDOWN:

                if event.key == K_ESCAPE:
                    quit_pygame()
                    quit()

                elif event.key == K_j:
                    self.decelerate_left_shoot()

                elif event.key == K_k:

                    if not self.midair:
                        self.y_speed += self.jump_dy

        ###

        pressed_state = get_pressed_state()

        if pressed_state[K_d]:

            self.x_accel = min(self.x_accel + 1, 0)

            if self.x_speed >= 0:
                self.set_state('walk_right')

        elif pressed_state[K_a]:
            self.x_accel += -1
            self.set_state('walk_left')

        elif self.x_speed == 0:
            self.set_state('idle_left')

    def decelerate_left_update(self):

        x = self.rect.x

        self.x_speed += self.x_accel
        self.rect.x += self.x_speed

        if self.x_speed > 0:
            self.x_speed += -1
        elif self.x_speed < 0:
            self.x_speed += 1

        if self.rect.x != x:
            self.avoid_blocks_horizontally()

        self.react_to_gravity()

        if get_msecs() - self.last_damage > DAMAGE_REBOUND_MSECS:
            self.aniplayer.restore_constant_drawing()

    def decelerate_left_shoot(self):

        pos_value = self.rect.move(0, -2).midleft
        projectile = DefaultProjectile(x_orientation=-1, pos_name='center', pos_value=pos_value)
        PROJECTILES.add(projectile)
        self.aniplayer.blend('+shooting')
