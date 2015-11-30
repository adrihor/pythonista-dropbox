import dropbox
from pythonista_dropbox.request_auth_token import (
    keychain,
    get_session,
)

keychain_key_words = (
    ('dmmmd sync', 'access token key', ),
    ('dmmmd sync', 'access token secret', ),
)
ACCESS = ACCESS_KEY, ACCESS_SECRET = [keychain.get_password(service, account)
                                      for service, account
                                      in keychain_key_words]
assert all(ACCESS), "Run request-auth-token to set access key and secret."


def get_client(access_key=None, access_secret=None):
    """returns a dropbox client
    """
    access_key = ACCESS_KEY if access_key is None else access_key
    access_secret = ACCESS_SECRET if access_secret is None else access_secret
    session = get_session()
    session.set_token(access_key, access_secret)
    client = dropbox.client.DropboxClient(session)
    return client
