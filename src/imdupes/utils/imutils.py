import imagehash
import numpy
from imagehash import ImageHash, MeanFunc
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
        hash_value = imagehash.phash(im.getchannel('R'), hash_size=int(hash_size / 4)).__str__()
        hash_value += imagehash.phash(im.getchannel('G'), hash_size=int(hash_size / 4)).__str__()
        hash_value += imagehash.phash(im.getchannel('B'), hash_size=int(hash_size / 4)).__str__()
        hash_value += imagehash.phash(im.getchannel('A'), hash_size=int(hash_size / 4)).__str__()
        return hash_value

    elif method == HashingMethod.RGB:
        im = image if image.mode == 'RGB' else image.convert('RGB')
        hash_value = imagehash.phash(im.getchannel('R'), hash_size=int(hash_size / 3)).__str__()
        hash_value += imagehash.phash(im.getchannel('G'), hash_size=int(hash_size / 3)).__str__()
        hash_value += imagehash.phash(im.getchannel('B'), hash_size=int(hash_size / 3)).__str__()
        return hash_value

    elif method == HashingMethod.BW:
        return imagehash.average_hash(image, hash_size=hash_size).__str__()

    elif method == HashingMethod.BW_HIST:
        hash_value = imagehash.average_hash(image, hash_size=hash_size).__str__()
        hash_value += average_histogram_hash(image).__str__()
        return hash_value

    else:
        raise ValueError(f'Unknown HashingMethod "{method.value}"')


def average_histogram_hash(
        image: Image,
        mask: Image = None,
        extrema: tuple[int, int] | tuple[float, float] = None,
        mean: MeanFunc = numpy.mean
) -> ImageHash:
    """
    Average Histogram computation using imagehash.Image.histogram().

    A bilevel image (mode "1") is treated as a greyscale ("L") image by this function.

    Takes the color histogram data, where for each data point, assign it a 1 or 0 based on if it is larger than the
    global average or not. Then treats this stream of data as a string of bits to be converted to imagehash.ImageHash.

    Takes all arguments available to imagehash.Image.histogram().

    @image must be a PIL instance.
    @mean how to determine the average luminescence. can try numpy.median instead.
    """

    hist = numpy.asarray(image.histogram(mask, extrema))
    avg = mean(hist)
    diff = hist > avg
    return ImageHash(diff)
