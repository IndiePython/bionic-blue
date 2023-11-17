

class SwitchStateException(Exception):
    """Raised to switch to new given state."""

    def __init__(self, new_state):

        self.state = new_state
        super().__init__("Must switch to new given state.")


class SwitchModeException(Exception):
    """Raised to switch between normal/play/record mode."""

    def __init__(self, mode_name):

        self.mode_name = mode_name
        super().__init__("Must switch to new mode.")
