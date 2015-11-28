try:
    import urllib3.contrib.pyopenssl
    urllib3.contrib.pyopenssl.inject_into_urllib3()
except ImportError:
    pass
from pythonista_dropbox.adapters import PythonistaModuleAdapter
import dropbox
import json
import sys
import urllib
try:  # keychain on non-Pythonista is called keyring
    import keyring
except ImportError:
    keyring = None

modules = ('webbrowser', 'clipboard', 'keychain')
webbrowser, clipboard, keychain = [PythonistaModuleAdapter(module) for module
                                   in modules]
if keychain.platform.pythonista:
    dropbox_dropbox_pwd = keychain.get_password('dropbox', 'dmmmd')
    APP_KEY = keychain.get_password('dmmmd_sync', 'app_key')
    APP_SECRET = keychain.get_password('dmmmd_sync', 'app_secret')
else:
    dropbox_pwd = ''
    APP_KEY = ''
    APP_SECRET = ''
sensitive_info = (
    ('dropbox password', dropbox_pwd, ),
    ('dropbox app key', APP_KEY, ),
    ('dropbox app secret', APP_SECRET, )
)

ACCESS_TYPE = 'dropbox'


def get_session():
    names, variables = zip(*sensitive_info)
    if not all(variables):
        values = []
        for name, string in sensitive_info:
            if not string:
                values.append(raw_input("Please enter the {}: ".format(name)))
        variables = values

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
        print("open this url:", url)
        webbrowser.open(url)
        clipboard.set(dropbox_pwd)
        raw_input()
    except dropbox.rest.ErrorResponse as err:
        print(err.body)
        raise dropbox.rest.ErrorResponse(err)
    try:
        access_token = session.obtain_access_token(request_token)
        keys = ('key', 'secret',)
        creds = dict(zip(keys, [getattr(access_token, attr) for attr in keys]))
        creds = json.dumps(creds)
        if not webbrowser.platform.pythonista:
            print(creds)
        else:
            url = 'drafts4://x-callback/create?text={0}'.format(
                urllib.quote(creds))
            webbrowser.open(url)
        return 0
    except dropbox.rest.ErrorResponse as err:
        print(err.body)
        raise dropbox.rest.ErrorResponse(err)

if __name__ == "__main__":
    sys.exit(main())
