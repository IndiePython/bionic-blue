
### third-party imports

from pygame.locals import (

    QUIT,

    KEYDOWN,
    K_ESCAPE,
)


### local imports

from ....config import quit_game

from ....pygamesetup import SERVICES_NS


class Dead:

    def dead_control(self):

        for event in SERVICES_NS.get_events():

            if event.type == QUIT:
                quit_game()

            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                quit_game()

    def dead_update(self): pass
