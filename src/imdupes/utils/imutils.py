import imagehash
from PIL import Image

from utils.globs import HashingMethod
from utils.globs import DEFAULT_HASH_SIZE


class ImageFileWrapper:
    def __init__(self, image: Image = None, path: str = None):
        self.image = image
        self.path = path


def hash_image(
        image: Image,
        method: HashingMethod,
        hash_size: int = DEFAULT_HASH_SIZE
) -> str:
    if method == HashingMethod.RGBA:
        im = image if image.mode == 'RGBA' else image.convert('RGBA')

        hash_value = imagehash.phash(im.getchannel('R'), hash_size=hash_size).__str__()
        hash_value += imagehash.phash(im.getchannel('G'), hash_size=hash_size).__str__()
        hash_value += imagehash.phash(im.getchannel('B'), hash_size=hash_size).__str__()
        hash_value += imagehash.phash(im.getchannel('A'), hash_size=hash_size).__str__()

        return hash_value

    if method == HashingMethod.RGB:
        im = image if image.mode == 'RGB' else image.convert('RGB')

        hash_value = imagehash.phash(im.getchannel('R'), hash_size=hash_size).__str__()
        hash_value += imagehash.phash(im.getchannel('G'), hash_size=hash_size).__str__()
        hash_value += imagehash.phash(im.getchannel('B'), hash_size=hash_size).__str__()

        return hash_value

    if method == HashingMethod.BW:
        return imagehash.phash(image, hash_size=hash_size).__str__()
