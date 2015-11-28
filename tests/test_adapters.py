from pythonista_dropbox.adapters import (
    Platform,
    PythonistaModuleAdapter
)


def test_platform():
    """Test instance of Platform. """
    platform = Platform()

    assert platform.pythonista is False


def test_modules():
    """Test passing args and kwargs to a PythonistaModuleAdapter instance."""
    for module in ('webbrowser', 'clipboard'):
        pythonista_module = PythonistaModuleAdapter(module)

        url = "drafts4://x-callback/create?text={}"
        # example names of functions a module may have
        module_functions = ('open', 'get', 'set')
        arguments = (url, ) * 2
        kwordarguments = ({'url': url}, )
        for module_function in module_functions:
            function = getattr(pythonista_module, module_function)

            results = [function(*arg) for arg in arguments]
            assert not all(results)

            results = [function(**kwargs) for kwargs in kwordarguments]
            assert not all(results)


def test_module_object_function_override():
    """Test that if a the PythonistaModuleAdapter has an overridden function
    that function returns as expected when called."""

    def open(self, url):
        return url

    PythonistaModuleAdapter.open = open
    webbrowser = PythonistaModuleAdapter('webbrowser')
    url = 'drafts4://x-callback/create?text={}'

    assert webbrowser.open(url) == url
