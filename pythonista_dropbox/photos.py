import sys
import os
from pythonista_dropbox.adapters import PythonistaModuleAdapter

photos = PythonistaModuleAdapter('photos')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
mock_photo = os.path.join(BASE_DIR, 'mock_photo')
photo_meta_data = os.path.join(mock_photo, 'exifs')
images_dir = os.path.join(mock_photo, 'images')


kwargs = dict(
    show_albums=True,
    include_metadata=True,
    original=False,
    raw_data=True,
    multi=True
)


def pick_image(
    *args,
    **kwargs

):
    """Docstring for pick_image.
    Mock out the Pythonista version of photos.pick_image
    Return what picker in iOS would return
    """
    import json

    StringIO = PythonistaModuleAdapter('StringIO')
    if not StringIO.pythonista:
        from io import BytesIO
        StringIO.StringIO = BytesIO 
    else:
        from StringIO import StringIO as _StringIO
        StringIO.StringIO = _StringIO

    exifs = []
    for root, dirs, files in os.walk(photo_meta_data):
        for file in files:
            with open(os.path.join(photo_meta_data, file), 'r') as fh:
                exifs.append(json.load(fh))
    images = []
    for root, dirs, files in os.walk(images_dir):
        for file in files:
            with open(os.path.join(images_dir, file), 'r') as fh:
                binary_image = StringIO(fh.read())
            binary_image.seek(0)
            images.append(binary_image)
    if kwargs['raw_data']:
        """mocked photos and mocked meta_data like that returned 
        in Pythonista photos.pick_image"""
        return ((binary_image, photo_meta_data)
                for binary_image, photo_meta_data
                in zip(images, exifs))
    else:
        return ((type('JPEGImage', (), {})(), photo_meta_data)
                for photo_meta_data in exifs)

if not photos.pythonista:
    photos.pick_image = pick_image


def get_image_names():
    """A function that returns a tuple of filenames and their extensions as lists
    """
    kwargs['raw_data'] = False
    selected_photos = photos.pick_image(**kwargs)
    filenames = [meta_data['filename'].split('.')
                 for _, meta_data in selected_photos]
    names, extensions = zip(*filenames)
    return names, extensions


def main():
    import json
    import urllib
    webbrowser = PythonistaModuleAdapter('webbrowser')
    result = get_image_names()
    result = json.dumps(result)
    url = 'drafts4://x-callback/create?text={}'.format(
        urllib.quote(result))
    webbrowser.open(url)
    return 0

    if __name__ == "__main__":
        sys.exit(main())
