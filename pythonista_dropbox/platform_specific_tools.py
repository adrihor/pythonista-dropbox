import platform


class Platform(object):
    platform = platform.platform()

    """Use to distinguish Pythonista interpreter from non-Pythonista
    interpreter."""

    def __init__(self):
        """set pythonista to True if on iOS device"""
        if "Darwin-15.0.0" in self.platform:
            self.pythonista = True
        else:
            self.pythonista = False


