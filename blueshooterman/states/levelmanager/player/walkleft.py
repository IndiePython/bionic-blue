
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

from ....config import PROJECTILES, MAX_X_SPEED, SHOOTING_STANCE_MSECS

from .projectiles.default import DefaultProjectile



class WalkLeft:

    def walk_left_control(self):

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
                    self.walk_left_shoot()

                elif event.key == K_k:
                    self.jump()

        ###

        pressed_state = get_pressed_state()

        if pressed_state[K_a]:
            self.x_accel = max(self.x_accel - 1, -2)

        elif pressed_state[K_d]:

            self.x_accel += 1

            if self.aniplayer.anim_name == 'shooting_walk_left':
                self.set_state('decelerate_left')
                self.aniplayer.blend('+shooting')
            else:
                self.set_state('decelerate_left')

        else:
            self.x_accel = max(self.x_accel + 1, 0)

    def walk_left_update(self):

        if self.x_speed < 0:
            self.x_speed += -1

        self.x_speed += self.x_accel
        self.x_speed = min(max(self.x_speed, -MAX_X_SPEED), 0)

        self.rect.x += self.x_speed

        if not self.x_speed: self.set_state('idle_left')

        if get_msecs() - self.last_shot >= SHOOTING_STANCE_MSECS:
            self.aniplayer.blend('-shooting')

    def walk_left_shoot(self):

        pos_value = self.rect.move(0, -2).midleft
        projectile = DefaultProjectile(x_orientation=-1, pos_name='center', pos_value=pos_value)
        PROJECTILES.add(projectile)
        self.aniplayer.ensure_animation('shooting_walk_left')
        self.last_shot = get_msecs()
