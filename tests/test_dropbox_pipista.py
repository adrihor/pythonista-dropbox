import os
from pythonista_dropbox import dropbox_pipista


filename = 'hello_world-0.1.0.tar.gz'
tarball_path = os.path.join(
    '/PyPi-tarballs/',
    filename
)
source_dict = dict(
    url=tarball_path,
    filename=filename,
)


def test_dropbox_package_install():
    """test if a tarball can be downloaded with pipista"""
    assert dropbox_pipista.pypi_download(source_dict)
    assert os.path.exists(filename)


def test_install():
    """attempt an install"""
    result = dropbox_pipista.pypi_install(source_dict)

    is_true = result is True

    assert is_true


def main():
    pipista.pypi_install(source_dict)
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
