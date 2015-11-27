# -*- coding: utf-8 -*-
# Include the Dropbox SDK
import dropbox
from dropbox.rest import ErrorResponse
import os
import sys
from environment import dropbox_apps, DEFAULT, default_app
from environment import TOKEN_SUFFIX, DROPBOX_APPS_FILEPATH
# from environment import get_safe_dir_name


import pprint
pp = pprint.PrettyPrinter(indent=4)
TOKEN_DIRNAME = DROPBOX_APPS_FILEPATH
TOKEN_FILENAME = None
app = None


def get_client(_app=default_app):
    """returns an authorized dropbox client"""
    global TOKEN_FILENAME
    global app
    app = _app
    if os.path.exists(TOKEN_DIRNAME) is False:
        os.makedirs(TOKEN_DIRNAME)
    TOKEN_FILENAME = os.path.join(
        TOKEN_DIRNAME, get_safe_dir_name(app.name) + TOKEN_SUFFIX)
    try:
        # no exception if OAuth2 supported
        from dropbox.client import DropboxOAuth2FlowNoRedirect
        access_token = get_or_create_and_save_access_token()
        client = dropbox.client.DropboxClient(access_token)
    except ImportError:  # no DropboxOAuth2FlowNoRedirect
        session = request_session()
        client = dropbox.client.DropboxClient(session)
    return client

def request_split_token(session):
    """request a token with key, secret attrs and return it"""
    request_token = session.obtain_request_token()
    authorize_url = session.build_authorize_url(request_token)
    user_authorize(authorize_url)
    # Keeps browser open in Pythonista but only with no message
    raw_input()
    return session.obtain_access_token(request_token)


def user_authorize(authorize_url):
    """takes the user through authorization of app"""
    launch_browser(authorize_url)


def file_does_not_exist(e):
    import errno
    return errno.ENOENT == e.errno


def create_and_save_access_token():
    access_token = request_noredirect_access_token()
    save_access_token(access_token)
    return access_token


def get_or_create_and_save_access_token():
    """returns a stored token or takes user through authorization process"""
    try:  # to read from file
        token = read_token()
        if token != '':  # not empty, return token
            return token
        else:
            return create_and_save_access_token()
    except Exception as e:  # authorize a new one
        if file_does_not_exist(e):
            return create_and_save_access_token()


def read_token():
    with open(TOKEN_FILENAME, 'r') as fh:
        return fh.readline().strip()


def save_access_token(access_token):
    """saves string access_token to file TOKEN_FILENAME"""
    with open(TOKEN_FILENAME, 'w') as fh:
        fh.write(access_token)
    chmod_to_readonly()


def chmod_to_readonly():
    import stat
    import os

    os.chmod(TOKEN_FILENAME, stat.S_IREAD)


def request_session():
    """method for dropbox modules that don't have NO redirect
    such as Pythonista dropbox module to request access token
    """
    session = dropbox.session.DropboxSession(*app.session_credentials)
    key, secret = get_or_create_split_token(session)
    session.set_token(key, secret)
    return session


def get_or_create_split_token(session):
    """return key,secret from stored or created source"""
    try:  # read from file
        key, secret = read_pythonista_access_token()
    except:  # not in file
        access_token = request_split_token(session)
        # save to file
        text = "{access_token.key}|{access_token.secret}".format(
            access_token=access_token)
        save_access_token(text)
        key, secret = (access_token.key, access_token.secret)
    return key, secret


def read_pythonista_access_token():
    """reads token from file, if no file, makes a new request"""
    try:  # to read from file
        access_token = read_token()
        key, secret = access_token.split('|')
        return key, secret
    except Exception as e:  # authorize a new one
        if file_does_not_exist(e):
            raise


def request_noredirect_access_token():
    """request an access token for a dropbox app"""
    flow = dropbox.client.DropboxOAuth2FlowNoRedirect(
        *app.noredirect_credentials)
    authorize_url = flow.start()
    access_token = flow_user_authorize(authorize_url, flow)
    return access_token


def flow_user_authorize(authorize_url, flow):
    """launches a browser, if the browser cannot process the url,
    hit enter and do it manually. This happens with cli browsers."""
    launch_browser(authorize_url)
    message = "Enter the authorization code here. Enter if no code yet.: "
    code = raw_input(message).strip()

    if code == '':  # if browser not able to give code as in cli with elinks
        # This will fail if the user enters an invalid authorization code
        for line in flow_browser_message(authorize_url):
            print line
        code = raw_input("Enter the authorization code here: ").strip()
    access_token, user_id = flow.finish(code)
    return access_token


def launch_browser(url):
    import webbrowser
    webbrowser.open(url)


def flow_browser_message(authorize_url):
    message = []
    # Have the user sign in and authorize this token
    message.append('1. Go to: ' + authorize_url)
    message.append('2. Click "Allow" (you might have to log in first)')
    message.append('3. Copy the authorization code.')
    return message


def main(app_name=DEFAULT):
    app = dropbox_apps.get(app_name)
    try:
        client = get_client(app)
        print 'linked account: '
        pp.pprint(client.account_info())
        return client
    except ErrorResponse as e:
        if e.status == 401:
            print e.reason
            os.remove(TOKEN_FILENAME)
            main()


def test_deauthorized_token():
    client = main()
    client.disable_access_token()


if __name__ == '__main__':
    try:
        app_name = sys.argv[1]
        main(app_name)
    except IndexError:
        client = main()
