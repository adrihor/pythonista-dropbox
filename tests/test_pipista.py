import os
from pythonista_dropbox import pipista


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
    assert pipista.pypi_download(source_dict)
    assert os.path.exists(filename)


def test_install():
    """attempt an install"""
    result = pipista.pypi_install(source_dict)

    is_true = result is True

    assert is_true
