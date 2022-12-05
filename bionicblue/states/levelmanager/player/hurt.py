
### third-party imports

from pygame import quit as quit_pygame

from pygame.locals import (

    QUIT,

    KEYDOWN,
    K_ESCAPE,
)

from pygame.event import get as get_events

from pygame.time import get_ticks as get_msecs


### local import
from ....config import DAMAGE_STANCE_MSECS, DAMAGE_REBOUND_MSECS


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

    def hurt_update(self):

        x = self.rect.x

        self.rect.x += self.x_speed

        if get_msecs() - self.last_damage >= DAMAGE_STANCE_MSECS:

            self.x_speed = 0
            new_state = 'idle_right' if self.aniplayer.anim_name.endswith('right') else 'idle_left'
            self.set_state(new_state)

        if self.rect.x != x:
            self.avoid_blocks_horizontally()

        self.react_to_gravity()

        if get_msecs() - self.last_damage > DAMAGE_REBOUND_MSECS:
            self.aniplayer.restore_constant_drawing()
