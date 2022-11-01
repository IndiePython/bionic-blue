
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
from ....config import DAMAGE_STANCE_MSECS


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

        self.rect.x += self.x_speed

        if get_msecs() - self.last_damage >= DAMAGE_STANCE_MSECS:

            new_state = 'idle_right' if self.aniplayer.anim_name.endswith('right') else 'idle_left'
            self.set_state(new_state)
