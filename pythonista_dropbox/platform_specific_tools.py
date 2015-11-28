import platform
import importlib


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


class ModuleObject(object):
    platform = Platform()

    """substitute for Pythonisa-only modules to aid in Pythonista development
    on non-iOS platform, instantiate and then can mock any function on the module"""

    def __init__(self, module):
        if self.platform.pythonista:
            imported_module = importlib.import_module(module)
            setattr(self, module, imported_module)
        else:
            setattr(self, module, type('MockWebbrowser', (), {})())
        self.module = module

    def mock_function(self, *args, **kwargs):
        return

    def __getattr__(self, attr):
        """returns attr of webbrowser module if Pythonista
        """
        try:
			attrs = getattr(getattr(self, self.module), attr)
            return attr
        except AttributeError:
            return self.mock_function
