"""General configuration for game."""

### standard library imports

from types import SimpleNamespace

from pathlib import Path


###

REFS = SimpleNamespace()
REFS.states = SimpleNamespace()

REFS.data = {
    'level': 'intro.lvl',
    'health': 100,
}

REFS.enable_player_tracking = (
    lambda: REFS.states.level_manager.enable_player_tracking()
)

REFS.disable_player_tracking = (
    lambda: REFS.states.level_manager.disable_player_tracking()
)

###

GRAVITY_ACCEL = 2
MAX_Y_SPEED = 10
MAX_X_SPEED = 4

SHOOTING_STANCE_MSECS = 300
DAMAGE_STANCE_MSECS = 400
DAMAGE_REBOUND_MSECS = 800

BLOCKS = set()
ACTORS = set()
PROJECTILES = set()
FRONT_PROPS = set()

BLOCKS_ON_SCREEN = set()
ACTORS_ON_SCREEN = set()

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

NO_ALPHA_IMAGES_DIR = IMAGES_DIR  / 'no_alpha'
ALPHA_IMAGES_DIR = IMAGES_DIR  / 'alpha'

###

SURF_MAP = {}
ANIM_DATA_MAP = {}
SOUND_MAP = {}
