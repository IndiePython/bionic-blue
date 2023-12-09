

class SwitchStateException(Exception):
    """Raised to switch to new given state."""

    def __init__(self, new_state):

        self.state = new_state
        super().__init__("Must switch to new given state.")


class BackToBeginningException(Exception):
    """Raised to go back to beginning of the game loop.

    Works just like the "continue" statement within a while-loop
    or for-loop. That is, it just serves to go back to the top
    of the iteration.
    """

class SwitchModeException(Exception):
    """Raised to switch between normal/play/record mode."""

    def __init__(self, mode_name):

        self.mode_name = mode_name
        super().__init__("Must switch to new mode.")
