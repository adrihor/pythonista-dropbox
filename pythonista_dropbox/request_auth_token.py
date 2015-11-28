try:
    import urllib3.contrib.pyopenssl
    urllib3.contrib.pyopenssl.inject_into_urllib3()
except ImportError:
    pass

from pythonista_dropbox.platform_specific_tools import ModuleObject
import dropbox
import json
import sys
import urllib

webbrowser, clipboard  = [ModuleObject(module) for module 
                          in ('webbrowser', 'clipboard')]
pwd = 'hx7wcgAYoreRt2ivJwYkznkqpzXR'
APP_KEY = 'wslawux2b38q2j3'
APP_SECRET = 'qb4yg62ea9hho70'
ACCESS_TYPE = 'dropbox'


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
        print("open this url:", url)
        webbrowser.open(url)
        clipboard.set(pwd)
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
            url = 'drafts4://x-callback/create?text={0}'.format(urllib.quote(creds))
            webbrowser.open(url)
        return 0
    except dropbox.rest.ErrorResponse as err: 
        print(err.body)
        raise dropbox.rest.ErrorResponse(err)

if __name__ == "__main__":
    sys.exit(main())
