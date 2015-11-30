from pythonista_dropbox.photos import photos
from pythonista_dropbox import photos as photo_module

kwargs = dict(
    show_albums=True,
    include_metadata=True,
    original=True,
    raw_data=True,
    multi=True
)
extension_names = (
    'JPG',
    'GIF',
)


def test_photos():
    """TODO: Docstring for test_photos.
    :returns: TODO

    """
    if not photos.pythonista:
        assert photos.pick_image
    selected_photos = photos.pick_image(**kwargs)
    for binary_image, meta_info in selected_photos:
        assert binary_image
        assert 'JPG' in meta_info.get('filename')


def test_get_image_names():
    """Test that get_image_names returns a list of filenames

    """
    names, extensions = photo_module.get_image_names()
    assert all('IMG' in name for name in names)
    assert all(extension in extension_names for extension in extensions)
