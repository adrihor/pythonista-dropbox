from pythonista_dropbox.adapters import PythonistaModuleAdapter
try:
    import keyring
except ImportError:
    import keychain as keyring
import sys

keychain = PythonistaModuleAdapter('keychain')
keychain.keychain = keyring


def set(services, accounts):
    """set the keychain passwords with user input"""
    for service, account in zip(services, accounts):
        value = raw_input(
            "Enter the info for {0}:{1}: ".format(service, account))
        keychain.set_password(service, account, value)


def main():
    from pythonista_dropbox.request_auth_token import services, accounts
    set(services, accounts)
    return 0


if __name__ == "__main__":
    sys.exit(main())
