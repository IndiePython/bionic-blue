
### third-party imports

from pygame import quit as quit_pygame

from pygame.locals import (

    QUIT,

    KEYDOWN,
    KEYUP,
    K_j,
    K_ESCAPE,

)

from pygame.event import get as get_events


### local import

from ....config import (
    REFS,
    DAMAGE_STANCE_MSECS,
    DAMAGE_REBOUND_MSECS,
)


class Hurt:

    def hurt_control(self):

        ###

        for event in get_events():

            if event.type == QUIT:
                quit_pygame()
                quit()

            elif event.type == KEYDOWN:

                if event.key == K_ESCAPE:
                    quit_pygame()
                    quit()

            elif event.type == KEYUP:

                if event.key == K_j:
                    self.stop_charging()

    def hurt_update(self):

        x = self.rect.x

        self.rect.x += self.x_speed

        msecs = REFS.msecs

        if msecs - self.last_damage >= DAMAGE_STANCE_MSECS:

            self.x_speed = 0

            ap = self.aniplayer

            new_state = (
                'idle_right'
                if 'right' in ap.anim_name
                else 'idle_left'
            )

            self.set_state(new_state)

            ap.switch_animation(
                ##
                (
                    'idle_climbing_right'
                    if new_state == 'idle_right'
                    else 'idle_climbing_left'
                )
                if self.ladder

                ##
                else new_state

            )

        if self.charge_start:
            self.check_charge()

        if not self.ladder:

            if self.rect.x != x:
                self.avoid_blocks_horizontally()

            self.react_to_gravity()

        if msecs - self.last_damage > DAMAGE_REBOUND_MSECS:
            self.check_invisibility()
