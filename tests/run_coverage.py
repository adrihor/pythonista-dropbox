import pytest


def main():
    pytest.main('-s .')
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
