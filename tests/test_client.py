import os


def test_access_key_and_secret_set():
    """TODO: Docstring for test_access_key_and_secret_set.
    :returns: TODO

    """
    from pythonista_dropbox.client import keychain_key_words
    from pythonista_dropbox.client import keychain

    access = [keychain.get_password(service, account)
              for service, account in keychain_key_words]
    assert all(access), "Run main in request_auth_token to set access."


def test_client():
    from pythonista_dropbox.client import get_client
    client = get_client()

    path = "Public"
    public_metadata = client.metadata(path)

    assert public_metadata.get('root') == 'dropbox'
    assert public_metadata.get('path') == os.path.join('/', path)
