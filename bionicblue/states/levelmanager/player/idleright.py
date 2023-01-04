
### third-party imports

from pygame import quit as quit_pygame

from pygame.locals import (

    QUIT,
    K_a, K_d,

    KEYDOWN,
    KEYUP,
    K_ESCAPE,
    K_j, K_k,

)

from pygame.event import get as get_events

from pygame.key import get_pressed as get_pressed_state


### local imports

from ....config import (
    REFS,
    PROJECTILES,
    SHOOTING_STANCE_MSECS,
    DAMAGE_REBOUND_MSECS,
)

from .projectiles.default import DefaultProjectile



class IdleRight:

    def idle_right_control(self):

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
                    self.idle_right_shoot()

                elif event.key == K_k:
                    self.jump()

            elif event.type == KEYUP:

                if event.key == K_j:

                    result = self.stop_charging()

                    if result:
                        self.idle_right_release_charge(result)
        ###

        pressed_state = get_pressed_state()

        if pressed_state[K_a]:

            self.x_accel += -1
            self.set_state('walk_left')

        elif pressed_state[K_d]:

            self.x_accel += 1
            self.set_state('walk_right')

    def idle_right_update(self):

        x = self.rect.x

        msecs = REFS.msecs

        if msecs - self.last_shot >= SHOOTING_STANCE_MSECS:
            self.aniplayer.blend('-shooting')

        if self.charge_start:
            self.check_charge()

        if self.rect.x != x:
            self.avoid_blocks_horizontally()

        self.react_to_gravity()

        if msecs - self.last_damage > DAMAGE_REBOUND_MSECS:
            self.aniplayer.restore_constant_drawing()

    def idle_right_shoot(self):

        pos_value = self.rect.move(0, -2).midright
        projectile = DefaultProjectile(x_orientation=1, pos_name='center', pos_value=pos_value)
        PROJECTILES.add(projectile)
        self.aniplayer.blend('+shooting')
        self.charge_start = self.last_shot = REFS.msecs

    def idle_right_release_charge(self, charge_type):
        ...
