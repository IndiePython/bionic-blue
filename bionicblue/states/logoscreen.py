
### local imports
from itertools import repeat, chain


### third-party imports

from pygame.locals import QUIT

from pygame.display import update


### local imports

from ..config import REFS, SURF_MAP, quit_game

from ..pygamesetup import SERVICES_NS

from ..pygamesetup.constants import WHITE_BG, blit_on_screen

from ..exceptions import SwitchStateException



class LogoScreen:

    def prepare(self):

#        self.get_next_surf = iter(range(0)).__next__
        self.get_next_surf = chain.from_iterable(

            chain(repeat(SURF_MAP[key], 45), repeat(WHITE_BG, 1))
            for key in (
                'indiepython_logo.png',
                'python_logo.png',
                'pygame_logo.png',
            )

        ).__next__

    def control(self):

        for event in SERVICES_NS.get_events():

            if event.type == QUIT:
                quit_game()

    def update(self):
        pass

    def draw(self):

        blit_on_screen(WHITE_BG, (0, 0))

        try:
            blit_on_screen(self.get_next_surf(), (102, 30))

        except StopIteration:

            title_screen = REFS.states.title_screen
            title_screen.prepare()
            raise SwitchStateException(title_screen)

        update()
