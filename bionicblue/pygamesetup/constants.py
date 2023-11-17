
### standard library import
from functools import partial


### third-party imports

from pygame import (
    init as init_pygame,
    locals as pygame_locals,
)

from pygame.locals import (

    QUIT,
    KEYDOWN,

    K_F7,
    K_F8,

    SCALED,
    KMOD_NONE,

)

from pygame.mixer import pre_init as pre_init_mixer

from pygame.key import set_repeat

from pygame.time import Clock

from pygame.color import THECOLORS

from pygame.display import set_icon, set_caption, set_mode, update

from pygame.image import load as load_image

from pygame.event import get



### local imports
from ..config import DATA_DIR, quit_game



### pygame initialization setups

## pygame mixer pre-initialization
pre_init_mixer(frequency=44100)


## pygame initialization
init_pygame()


### set icon and caption for window

image_path = str(DATA_DIR / "app_icon.png")
#set_icon(load_image(image_path))


### create/set screen

SIZE = (320, 180)

SCREEN = set_mode(SIZE, SCALED)

SCREEN.fill(THECOLORS['white'])
WHITE_BG = SCREEN.copy()

SCREEN_RECT = SCREEN.get_rect()


set_caption('Bionic Blue', 'BB')

blit_on_screen = SCREEN.blit

screen_colliderect = SCREEN_RECT.colliderect



### framerate-related values/objects

FPS = 30

MSECS_PER_FRAME = 1000 / FPS

_CLOCK = Clock()

maintain_fps = _CLOCK.tick
get_fps = _CLOCK.get_fps


### anonymous object to keep track of general values;
###
### values are introduced/update during app's usage:
### frame index is incremented, reset to -1, mode name
### is changed as we switch to other modes, etc.

GENERAL_NS = type("Object", (), {})()

GENERAL_NS.frame_index = -1
GENERAL_NS.mode_name = 'normal'


### name of key pygame services used by all different modes

GENERAL_SERVICE_NAMES = (

    "get_events",

    "get_pressed_keys",
    "get_pressed_mod_keys",

    "get_mouse_pos",
    "get_mouse_pressed",

    "set_mouse_pos",
    "set_mouse_visibility",

    "update_screen",

    "frame_checkups",

)


## event values to strip

EVENT_KEY_STRIP_MAP = {

  'MOUSEMOTION': {
    'buttons': (0, 0, 0),
    'touch': False,
    'window': None,
  },

  'MOUSEBUTTONDOWN': {
    'button': 1,
    'touch': False,
    'window': None,
  },

  'MOUSEBUTTONUP': {
    'button': 1,
    'touch': False,
    'window': None,
  },

  'KEYUP': {
    'mod': KMOD_NONE,
    'unicode': '',
    'window': None,
  },

  'KEYDOWN': {
    'mod': KMOD_NONE,
    'unicode': '',
    'window': None,
  },

  'TEXTINPUT': {
    'window': None,
  },

}

### event name to make compact

EVENT_COMPACT_NAME_MAP = {
    'KEYDOWN': 'kd',
    'KEYUP': 'ku',
    'TEXTINPUT': 'ti',
    'MOUSEMOTION': 'mm',
    'MOUSEBUTTONUP': 'mbu',
    'MOUSEBUTTONDOWN': 'mbd',
}

### key of events to make compact

EVENT_KEY_COMPACT_NAME_MAP = {

  'MOUSEMOTION': {
    'pos': 'p',
    'rel': 'r',
    'buttons': 'b',
    'touch': 't',
    'window': 'w',
  },

  'MOUSEBUTTONDOWN': {
    'pos': 'p',
    'button': 'b',
    'touch': 't',
    'window': 'w',
  },

  'MOUSEBUTTONUP': {
    'pos': 'p',
    'button': 'b',
    'touch': 't',
    'window': 'w',
  },

  'KEYUP': {
    'key': 'k',
    'scancode': 's',
    'mod': 'm',
    'unicode': 'u',
    'window': 'w',
  },

  'KEYDOWN': {
    'key': 'k',
    'scancode': 's',
    'mod': 'm',
    'unicode': 'u',
    'window': 'w',
  },

  'TEXTINPUT': {
    'text': 't',
    'window': 'w',
  },

}


### available keys

KEYS_MAP = {

    item : getattr(pygame_locals, item)

    for item in dir(pygame_locals)

    if item.startswith('K_')

}

SCANCODE_NAMES_MAP = {

    getattr(pygame_locals, name): name

    for name in dir(pygame_locals)

    if name.startswith('KSCAN')

}


MOD_KEYS_MAP = {

    item: getattr(pygame_locals, item)

    for item in dir(pygame_locals)

    if (
        item.startswith('KMOD')
        and item != 'KMOD_NONE'
    )

}



### function to pause when recording/playing session

class CancelWhenPaused(Exception):
    """Raised during pause to cancel and return to normal mode."""

def pause():

    running = True

    while running:

        ### keep constants fps
        maintain_fps(FPS)

        ### process events

        for event in get():

            if event.type == QUIT:
                quit_game()

            elif event.type == KEYDOWN:

                if event.key == K_F8:
                    running = False

                elif event.key == K_F7:
                    raise CancelWhenPaused

        ### update the screen
        update()

