"""Setup of different modes."""

### local imports

## constants

from .constants import (
    SCREEN,
    SCREEN_RECT,
    GENERAL_NS,
    GENERAL_SERVICE_NAMES,
    blit_on_screen,
)

## custom services
from .services import normal, record, play


### create a namespace to store the services in use
SERVICES_NS = type("Object", (), {})()

### set normal services on namespace (enables normal mode)
###
### there's no need to reset the window mode this first time,
### because it was already properly set in the constants.py
### sibling module
normal.set_behaviour(SERVICES_NS, reset_window_mode=False)


### function to switch modes

def switch_mode(mode_info_ns):
    """Switch to specific mode according to reset info data.

    Parameters
    ==========
    mode_info_ns (exceptions.SwitchModeException)
        has attributes containing data about mode to be
        switched to.
    """
    mode = GENERAL_NS.mode_name = mode_info_ns.mode_name

    if mode == 'record':
        record.set_behaviour(SERVICES_NS)

    elif mode == 'play':
        play.set_behaviour(SERVICES_NS)

    elif mode == 'normal':
        normal.set_behaviour(SERVICES_NS)
