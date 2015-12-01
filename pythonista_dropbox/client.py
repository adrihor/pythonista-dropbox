import dropbox
from pythonista_dropbox.request_auth_token import (
    keychain,
    get_session,
)

keychain_key_words = (
    ('default app', 'access token key', ),
    ('default app', 'access token secret', ),
)

ACCESS = ACCESS_KEY, ACCESS_SECRET = [keychain.get_password(service, account)
                                      for service, account
                                      in keychain_key_words]
assert all(ACCESS), \
    ' '.join((
        "Run request-auth-token at the"
        "command line to set access key and secret.",
        "Refer to https://www.dropbox.com/developers/reference/oauth-guide"
        "for detailed guidance."
    ))


def get_client(access_key=None, access_secret=None):
    """returns a dropbox client
    see https://www.dropbox.com/developers-v1/core/start/python
    """
    access_key = ACCESS_KEY if access_key is None else access_key
    access_secret = ACCESS_SECRET if access_secret is None else access_secret
    session = get_session()
    session.set_token(access_key, access_secret)
    client = dropbox.client.DropboxClient(session)
    return client
