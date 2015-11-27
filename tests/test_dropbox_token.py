import pytest

@pytest.mark.current
def test_Oauth_flow():
    with pytest.raises(ImportError):
        from dropbox.client import DropboxOAuth2FlowNoRedirect
