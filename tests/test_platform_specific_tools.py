import pytest
from pythonista_dropbox.platform_specific_tools import (
    Platform,
    ModuleObject
)



def test_platform():
    """test platform specific tools
    """

    platform = Platform()

    assert platform.pythonista is False


def test_modules():
    """returns a mockfunction that returns None on call"""
    for module in ('webbrowser', 'clipboard'):
        pythonista_module = ModuleObject(module)

        url = "drafts4://x-callback/create?text={}"
        result = pythonista_module.open(url)
        
        assert result is None

        result = pythonista_module.open(url=url)
        
        assert result is None

        result = pythonista_module.set(url)

        assert result is None
