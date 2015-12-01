from pythonista_dropbox.request_auth_token import services, accounts
from pythonista_dropbox import sensitive_data


def main():
    sensitive_data.set(services, accounts)
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
