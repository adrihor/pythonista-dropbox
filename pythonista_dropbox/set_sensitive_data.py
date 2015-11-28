from pythonista_dropbox.adapters import PythonistaModuleAdapter
from pythonista_dropbox.request_auth_token import services, accounts
try:
    import keyring
except ImportError:
    import keychain as keyring

keychain = PythonistaModuleAdapter('keychain')
keychain.keychain = keyring
for service, account in zip(services, accounts):
    value = raw_input("Enter the info for {0}:{1}: ".format(service, account))
    keychain.set_password(service, account, value)
