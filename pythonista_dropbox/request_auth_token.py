try:  # fix insecure warning in urllib3
    import urllib3.contrib.pyopenssl
    urllib3.contrib.pyopenssl.inject_into_urllib3()
except ImportError:
    pass
import sys
try:  # keychain on non-Pythonista is called keyring
    import keyring
except ImportError:
    import keychain as keyring
from pythonista_dropbox.adapters import Platform, PythonistaModuleAdapter

# mock the Pythonista modules
modules = (
    'webbrowser',
    'clipboard',
    'keychain',
    'dropbox',
    'console',
    )
webbrowser, clipboard, keychain, dropbox, console = [
    PythonistaModuleAdapter(module) for module
    in modules
]
platform = Platform()
if not platform.pythonista:
    raw_input = input
    """if not on iOS, use dropbox-sdk-python rather than PyPi dropbox SDK"""
    import dropbox as _dropbox
    dropbox.dropbox = _dropbox

    def _print(string, *args, **kwargs):
        print(string)
    console.alert = _print
if platform.pythonista:
    console_kwargs = {'hide_cancel_button': True}
    title = 'Please note:'
    button1 = "OK"
    message = None
    console_args = (title, message, button1)
else:
    console_kwargs, console_args = {}, (None, ) * 3


keychain.keychain = keyring  # differing name for keyrin in Pythonista
DEFAULT_APP = 'default app'
services = (  # keychain args
    'dropbox',
) + (DEFAULT_APP, ) * 3
accounts = (  # keychain args
    'password',
    'app key',
    'app secret',
    'oauth token',
)


ACCESS_TYPE = 'dropbox'
credentials = DROPBOX_PWD, APP_KEY, APP_SECRET, TOKEN = [
    keychain.get_password(service, account)
    for service, account
    in zip(services, accounts)
]
credentials_keys = \
    ('dropbox password', 'app key', 'app secret', 'oauth token'),
if platform.pythonista:
    # all except the last one, no 'oauth token'
    credentials_keys, credentials = [
        tuple(list(item)[:-1]) for item in (credentials_keys, credentials)
    ]
credentials = dict(zip(
    credentials_keys,
    credentials
))

try:
    assert all(credentials)
except AssertionError:
    message = "The credentials have not been set on the keyring: {0}".format(
        ', '.join([key for key, value in credentials.items() if not value]))
    _args = list(console_args)
    _args[1] = message
    _args = tuple(_args)
    console.alert(message, *_args, **console_kwargs)


def get_session():
    session = dropbox.session.DropboxSession(
        APP_KEY, APP_SECRET, ACCESS_TYPE)
    return session


def get_request_token(session):
    request_token = session.obtain_request_token()
    return request_token


def get_authorize_url(session, request_token):
    url = session.build_authorize_url(request_token)
    return url


def set_keyring(access_token):
    """set the access token key and access token secret to the keyring"""
    access_token_keys = ('key', 'secret',)
    app_accounts = [' '.join(('access token', access_token_key))
                    for access_token_key in access_token_keys]
    app_services = ('access token {0}', ) * 2
    app_services = [_service.format(_service) for _service in services[1:]]
    access_token = dict(zip(
        access_token_keys,
        [getattr(access_token, attr)
         for attr in access_token_keys]))
    for name, service, cred_key in zip(
        app_services,
        app_accounts,
        access_token_keys
    ):
        keychain.set_password(name, service, access_token[cred_key])

        _args = list(console_args)
        message = "The app {0} is in the keychain under ('{1}', '{2}')".\
            format(cred_key, name, service)
        _args[1] = message
        _args = tuple(_args)
        console.alert(*_args, **console_kwargs)


def main():
    """This main stores an access key and access token in the keyring
    using the arguments in services and accounts.
    This function has to be run prior to getting a client in client.py.
    """
    from pythonista_dropbox.client import get_client
    if not platform.pythonista:
        client = get_client(TOKEN)
        _args = list(console_args)
        _args[1] = str(client.users_get_current_account())
        _args = tuple(_args)
        console.alert(*_args, **console_kwargs)
        return
    try:
        session = get_session()
        request_token = get_request_token(session)
        url = get_authorize_url(session, request_token)
        # For easy pasting into web browser interface
        # in Pythonista, optional. It may be typed manually.
        clipboard.set(DROPBOX_PWD)
        print(', '.join(("open this url:", url)))
        webbrowser.open(url)
        raw_input()
    except dropbox.rest.ErrorResponse as err:
        print(err.body)
        message = \
            ' '.join((
                "Verify that your app access token is set on the keychain.",
                "Try running 'set-keychain' at the command line.",
                ))
        raise RuntimeError(message)
    try:
        access_token = session.obtain_access_token(request_token)
        set_keyring(access_token)
        return 0
    except dropbox.rest.ErrorResponse as err:
        print(err.body)
        raise RuntimeError()

if __name__ == "__main__":
    sys.exit(main())
