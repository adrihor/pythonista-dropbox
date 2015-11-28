from pythonista_dropbox.adapters import PythonistaModuleAdapter
try:
    import keyring
except:  # Pythonista version of keyring is called keychain
    import keychain as keyring


def test_keyring_keychain():
    """test using dot notation to set attrs to module that does not
    have the same name in both platforms"""
    keychain = PythonistaModuleAdapter('keychain')
    keychain.keychain = keyring

    assert keychain.keychain == keyring
    assert keychain.set_password == keyring.set_password
