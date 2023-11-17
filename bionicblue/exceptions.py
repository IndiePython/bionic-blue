

class SwitchStateException(Exception):
    """Raised to switch to new given state."""

    def __init__(self, new_state):

        self.state = new_state
        super().__init__("Must switch to new given state.")
