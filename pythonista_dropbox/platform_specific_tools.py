import platform
import importlib


class Platform(object):
    platform = platform.platform()

    """Use to distinguish Pythonista interpreter from non-Pythonista
    interpreter."""

    def __init__(self):
        """set pythonista to True if on iOS device
        assume that platform.platform returns a string with Darwin-15.0.0 in it"""
        self.pythonista = True if "Darwin-15.0.0" in self.platform else False


class PythonistaModuleAdapter(object):
    platform = Platform()

    """substitute for Pythonisa-only modules to aid in Pythonista development
    on non-iOS platform, instantiate and then can mock any function on the module"""

    def __init__(self, module):
        if self.platform.pythonista:
            imported_module = importlib.import_module(module)
            setattr(self, module, imported_module)
        else:
            setattr(self, module, type('MockModule', (), {})())
        self.module = module

    def mock_function(self, *args, **kwargs):
        return

    def __getattr__(self, attr):
        """Returns attr of module 'module' if has attr or mock_function if not.
        On non-Pythonista platform mock_function is returned. On Pythonista platform,
        the attr of the module is returned."""
        try:
            attrs = getattr(getattr(self, self.module), attr)
            return attr
        except AttributeError:
            return self.mock_function
