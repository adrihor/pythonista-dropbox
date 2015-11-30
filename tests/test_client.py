import os
from pythonista_dropbox.client import get_client


def test_client():
    client = get_client()

    path = "Public"
    public_metadata = client.metadata(path)

    assert public_metadata.get('root') == 'dropbox'
    assert public_metadata.get('path') == os.path.join('/', path)
