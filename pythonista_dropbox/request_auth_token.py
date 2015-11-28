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
import dropbox
from pythonista_dropbox.adapters import PythonistaModuleAdapter

modules = ('webbrowser', 'clipboard', 'keychain')
webbrowser, clipboard, keychain = [PythonistaModuleAdapter(module) for module
                                   in modules]
keychain.keychain = keyring  # differing name for keyrin in Pythonista
services = (
    'dropbox',
    'dmmmd sync',
    'dmmmd sync',
)
accounts = (
    'password',
    'app key',
    'app secret',
)

ACCESS_TYPE = 'dropbox'
DROPBOX_PWD, APP_KEY, APP_SECRET = [keychain.get_password(service, account)
                                    for service, account
                                    in zip(services, accounts)]


def get_session():
    session = dropbox.session.DropboxSession(
        APP_KEY, APP_SECRET, ACCESS_TYPE)
    return session


def get_client(session):
    client = dropbox.client.DropboxClient(session)
    return client


def get_request_token(session):
    request_token = session.obtain_request_token()
    return request_token


def get_authorize_url(session, request_token):
    url = session.build_authorize_url(request_token)
    return url


def main():
    try:
        session = get_session()
        request_token = get_request_token(session)
        url = get_authorize_url(session, request_token)
        clipboard.set(DROPBOX_PWD)  # for easy pasting into the HTML interface
        print("open this url:", url)
        webbrowser.open(url)
        raw_input()
    except dropbox.rest.ErrorResponse as err:
        print(err.body)
        raise RuntimeError()
    try:
        access_token = session.obtain_access_token(request_token)
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
            print("The app {0} is in the keychain under ('{1}', '{2}')".
                  format(cred_key, name, service))
        return 0
    except dropbox.rest.ErrorResponse as err:
        print(err.body)
        raise RuntimeError()

if __name__ == "__main__":
    sys.exit(main())
