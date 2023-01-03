
### local imports

from ..config import REFS

from .resourceloader import ResourceLoader

from .logoscreen import LogoScreen

from .levelmanager import LevelManager

from .hqmanager import HeadQuartersManager

#from .menuscreen import MenuScreen
#from .optionscreen import OptionsScreen
#from .endscreen import EndScreen


def setup_states():
    """Instantiate and store states."""
    states = REFS.states

    states.resource_loader = ResourceLoader()
    states.logo_screen = LogoScreen()
    states.level_manager = LevelManager()
    states.hq_manager = HeadQuartersManager()

    REFS.get_game_state = get_game_state

    #states.menu_screen = MenuScreen()
    #states.options_screen = OptionsScreen()

def get_game_state():
    """Pick appropriate gameplay state, prepare and return it."""
    return (
        REFS.states.level_manager
        if REFS.data['level_name'] == 'intro.lvl'
        else None # REFS.hq_loader
    )
