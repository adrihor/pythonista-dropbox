import sys
import os
from pythonista_dropbox.adapters import PythonistaModuleAdapter

photos = PythonistaModuleAdapter('photos')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
mock_photo = os.path.join(BASE_DIR, 'mock_photo')


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
    from StringIO import StringIO

    with open(os.path.join(mock_photo, 'photo_dict.json'), 'r') as fh:
        photo_meta_data = json.load(fh)
    with open(os.path.join(mock_photo, 'IMG_3008.jpeg'), 'r') as fh:
        binary_image = StringIO(fh.read())
        binary_image.seek(0)
    if kwargs['raw_data']:
        return ((binary_image, photo_meta_data), )
    else:
        return ((type('JPEGImage', (), {})(), photo_meta_data), )

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
    if not photos.pythonista:
        print(result)
    return 0

if __name__ == "__main__":
    sys.exit(main())
