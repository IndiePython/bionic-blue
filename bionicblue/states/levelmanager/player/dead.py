
### third-party imports

from pygame.locals import (

    QUIT,

    KEYDOWN,
    K_ESCAPE,
)

from pygame.event import get as get_events

from pygame.time import get_ticks as get_msecs


### local imports

from ....config import DAMAGE_STANCE_MSECS, quit_game

from ....pygamesetup import SERVICES_NS


class Dead:

    def dead_control(self):

        for event in SERVICES_NS.get_events():

            if event.type == QUIT:
                quit_game()

            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                quit_game()

    def dead_update(self): pass
