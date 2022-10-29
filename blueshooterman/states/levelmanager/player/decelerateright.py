
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


### local imports

from ....config import PROJECTILES

from .projectiles.default import DefaultProjectile



class DecelerateRight:

    def decelerate_right_control(self):

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
                    self.decelerate_right_shoot()

                elif event.key == K_k:

                    if not self.midair:
                        self.y_speed += self.jump_dy

        ###

        pressed_state = get_pressed_state()

        if pressed_state[K_a]:

            self.x_accel = max(self.x_accel - 1, 0)

            if self.x_speed <= 0:
                self.set_state('walk_left')

        elif pressed_state[K_d]:
            self.x_accel += 1
            self.set_state('walk_right')

        elif self.x_speed == 0:
            self.set_state('idle_right')

    def decelerate_right_update(self):

        self.x_speed += self.x_accel
        self.rect.x += self.x_speed

        if self.x_speed > 0:
            self.x_speed += -1
        elif self.x_speed < 0:
            self.x_speed += 1

    def decelerate_right_shoot(self):

        pos_value = self.rect.move(0, -2).midright
        projectile = DefaultProjectile(x_orientation=1, pos_name='center', pos_value=pos_value)
        PROJECTILES.add(projectile)
        self.aniplayer.blend('+shooting')
