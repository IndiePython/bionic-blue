"""Facility with function to run the Bionic Blue game.

Bionic Blue (by Kennedy Guerra): to know more about this game,
visit its website: https://bionicblue.indiepython.com
"""

### local imports

from .config import REFS

from .pygamesetup import SERVICES_NS, switch_mode

from .states import setup_states

from .exceptions import SwitchStateException, SwitchModeException


def run_game():
    """Run the game loop."""

    setup_states()

    state = REFS.states.resource_loader

    running = True

    while True:

        try:

            ### game loop

            while True:

                SERVICES_NS.frame_checkups()

                state.control()
                state.update()
                state.draw()

        except SwitchStateException as obj:
            state = obj.state

        except SwitchModeException as obj:
            switch_mode(obj)

if __name__ == '__main__':
    run_game()
