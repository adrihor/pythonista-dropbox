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
    'PNG',
)
extension_names = [name.lower() for name in extension_names]


def test_photos():
    """test that the PythonistaModuleAdapter mocking out Pythonista's
    photos.pick_image behaves in an expected way on non-Pythonista platform."""
    if not photos.pythonista:
        assert photos.pick_image
        selected_photos = photos.pick_image(**kwargs)
        for binary_image, meta_info in selected_photos:
            assert binary_image
            assert any([ext in meta_info.get('filename').lower()
                       for ext in extension_names])


def test_get_image_names():
    """Test that get_image_names returns a list of filenames

    """
    names, extensions = photo_module.get_image_names()
    assert any(['img' in name.lower()
                for name in names])
    assert all([extension.lower() in extension_names
                for extension in extensions])
