"""Facility with function to run the game."""

### local imports

from .config import REFS

from .pygameconstants import FPS, maintain_fps

from .states import setup_states


def run_game():
    """Run the game loop."""

    setup_states()

    state = REFS.states.resource_loader

    while True:

        maintain_fps(FPS)

        state.control()
        state.update()
        state.draw()

        state = state.next()
