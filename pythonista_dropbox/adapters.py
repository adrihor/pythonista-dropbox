import platform
import importlib


class Platform(object):
    """The Platform class is used to test if the Pythonista app is the
    interpreter based on 'Darwin-15.0.0.' presence in platform.platform()
    return value."""
    platform = platform.platform()

    def __init__(self):
        """Sets self.pythonista to True if on iOS device."""
        self.pythonista = True if "Darwin-15.0.0" in self.platform else False


class PythonistaModuleAdapter(object):
    """Class PythonistaModuleAdapter substitutes for Pythonisa-only
    modules to aid in Pythonista development on non-iOS platforms.
    Example usage for clipboard:
    DO NOT import the module clipboard.
    Instead, do this:
        clipboard = PythonistaModuleAdapter('clipboard')
    Now when you use clipboard on a non-Pythonista platform, any callable
    attribute of the equally named Pythonista module will accept all
    args and kwargs and return None.
    If the script is used in Pythonista, clipboard behaves exactly as if it
    were imported.
    To use in the case where the modules have differing names, do this:
        try:
            import keyring as keychain  # non-Pythonista
        except ImportError:
            import keychain # Pythonista

        keychain = PythonistaModuleAdapter('keychain')
        keychain.keychain = keyring"""
    platform = Platform()

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
        """Returns attr of module if has attr or mock_function if not.
        On non-Pythonista platform mock_function is returned.
        On Pythonista platform,
        the attr of the module is returned."""
        try:
            attrs = getattr(getattr(self, self.module), attr)
            return attrs
        except AttributeError:
            return self.mock_function
