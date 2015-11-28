import pytest

def test_Oauth_flow():
    from dropbox.client import DropboxOAuth2FlowNoRedirect

    assert DropboxOAuth2FlowNoRedirect
