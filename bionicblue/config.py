"""General configuration for game."""

### standard library imports

from types import SimpleNamespace

from pathlib import Path


### third-party import
from pygame import quit as quit_pygame


###
COLORKEY = (192, 192, 192)

###

REFS = SimpleNamespace(

    states = SimpleNamespace(),

    msecs = 0,

    data = {
        'level_name': 'intro.lvl',
        'health': 100,
    },

    enable_player_tracking = (
        lambda: REFS.states.level_manager.enable_player_tracking()
    ),

    disable_player_tracking = (
        lambda: REFS.states.level_manager.disable_player_tracking()
    ),

)

###


BLOCKS = set()
ACTORS = set()
PROJECTILES = set()
BACK_PROPS = set()
MIDDLE_PROPS = set()
FRONT_PROPS = set()

BACK_PROPS_ON_SCREEN = set()
BLOCKS_ON_SCREEN = set()
ACTORS_ON_SCREEN = set()
MIDDLE_PROPS_ON_SCREEN = set()

###

TASKS = []
append_task = TASKS.append
clear_tasks = TASKS.clear

def execute_tasks():

    if TASKS:

        for task in TASKS:
            task()

        clear_tasks()


###

DATA_DIR = Path(__file__).parent / 'data'

FONTS_DIR = DATA_DIR / 'fonts'
IMAGES_DIR = DATA_DIR / 'images'
ANIMATIONS_DIR = DATA_DIR / 'animations'
SOUNDS_DIR = DATA_DIR / 'sounds'
MUSIC_DIR = DATA_DIR / 'music'
LEVELS_DIR = DATA_DIR / 'levels'
PARTICLES_DIR = DATA_DIR / 'particles'

NO_ALPHA_IMAGES_DIR = IMAGES_DIR  / 'no_alpha'
ALPHA_IMAGES_DIR = IMAGES_DIR  / 'alpha'

###

SURF_MAP = {}
ANIM_DATA_MAP = {}
SOUND_MAP = {}

###

def quit_game():

    quit_pygame()
    quit()
