
### local imports
from itertools import repeat, chain


### third-party imports

from pygame import quit as quit_pygame

from pygame.locals import QUIT

from pygame.event import get as get_events

from pygame.time import get_ticks as get_msecs

from pygame.display import update


### local imports

from ..config import REFS, SURF_MAP

from ..pygameconstants import WHITE_BG, blit_on_screen

from ..textman import render_text


class LogoScreen:

    def __init__(self):
        self.next_state = self

    def prepare(self):

        self.get_next_surf = iter(range(0)).__next__
#        self.get_next_surf = chain.from_iterable(
#            chain(repeat(surf, 45), repeat(WHITE_BG, 1))
#            for surf in SURF_MAP.values()
#        ).__next__

    def control(self):

        for event in get_events():

            if event.type == QUIT:

                quit_pygame()
                quit()

    def update(self):
        pass

    def draw(self):

        try:
            blit_on_screen(self.get_next_surf(), (102, 30))

        except StopIteration:
            game_state = REFS.get_game_state()
            game_state.prepare()
            self.next_state = game_state

        update()

    def next(self):
        return self.next_state
