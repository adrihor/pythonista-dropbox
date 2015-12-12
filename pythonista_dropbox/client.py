import dropbox
from pythonista_dropbox.request_auth_token import (
    get_session,
    keychain,
    platform,
    set_keyring,
)
from contextlib import closing

keychain_key_words = (
    ('default app', 'access token key', ),
    ('default app', 'access token secret', ),
)

if not platform.pythonista:
    # need to put non-False values on keyring
    access_token = type(
        'AccessToken', (), {'key': 'mock key', 'secret': 'mock secret'})
    set_keyring(access_token)

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


if not platform.pythonista:
    def get_client_non_ios(token, *args):
        client = dropbox.Dropbox(token)

        compatibility_attrs = (
            ('metadata', 'files_get_metadata'),
        )

        for attr, function in compatibility_attrs:
            setattr(client, attr, getattr(client, function))
        return client

    get_client = get_client_non_ios
else:
    def _get_client(access_key=None, access_secret=None, *args):
        """returns a dropbox client
        see https://www.dropbox.com/developers-v1/core/start/python
        """
        access_key = ACCESS_KEY if access_key is None else access_key
        access_secret = ACCESS_SECRET if access_secret is None \
            else access_secret
        session = get_session()
        session.set_token(access_key, access_secret)
        client = dropbox.client.DropboxClient(session)
        return client

    get_client = _get_client
