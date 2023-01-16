"""Facility for function to initialize game."""

### standard library imports

from contextlib import redirect_stdout

from io import StringIO


### third-party imports

## our first pygame import has the stdout redirected,
## to prevent the default message to be printed on the
## screen;
##
## don't worry, we proudly credit the usage of pygame by
## displaying the pygame logo right upon launching the game,
## in the logo screen

with StringIO() as temp_stream:
    with redirect_stdout(temp_stream):
        from pygame import init as init_pygame

from pygame.mixer import pre_init as pre_init_mixer

from pygame.locals import SCALED

from pygame.display import set_mode, set_caption

from pygame.time import Clock

from pygame.color import THECOLORS



pre_init_mixer(frequency=44100)

init_pygame()

set_caption('Bionic Blue', 'BB')

SCREEN = set_mode((320, 180), SCALED, 32)
SCREEN.fill(THECOLORS['white'])

WHITE_BG = SCREEN.copy()
WHITE_BG.fill(THECOLORS['white'])

SCREEN_RECT = SCREEN.get_rect()
blit_on_screen = SCREEN.blit

screen_colliderect = SCREEN_RECT.colliderect

FPS = 30
MSECS_PER_FRAME = 1000 / FPS
maintain_fps = Clock().tick
