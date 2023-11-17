"""Facility with function to run the Bionic Blue game.

Bionic Blue (by Kennedy Guerra): to know more about this game,
visit its website: https://bionicblue.indiepython.com
"""

### third-party import
from pygame.time import get_ticks as get_msecs


### local imports

from .config import REFS

from .pygameconstants import FPS, maintain_fps

from .states import setup_states

from .exceptions import SwitchStateException


def run_game():
    """Run the game loop."""

    setup_states()

    state = REFS.states.resource_loader

    running = True

    while True:

        try:

            ### game loop

            while True:

                maintain_fps(FPS)

                REFS.msecs = get_msecs()

                state.control()
                state.update()
                state.draw()

        except SwitchStateException as obj:
            state = obj.state

if __name__ == '__main__':
    run_game()
