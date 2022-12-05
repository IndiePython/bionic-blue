
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


class Dead:

    def dead_control(self):

        for event in get_events():

            if event.type == QUIT:
                quit_pygame()
                quit()

            elif event.type == KEYDOWN:

                if event.key == K_ESCAPE:
                    quit_pygame()
                    quit()

    def dead_update(self): pass
