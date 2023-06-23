import sys
import imagehash
import numpy
from imagehash import ImageHash, MeanFunc
from PIL import Image
from tqdm.auto import tqdm
from termcolor import colored

from utils import loop_errprint
from utils.globs import HashingMethod
from utils.globs import AutoHashSize
from utils.globs import DEFAULT_HASH_SIZE
from utils.globs import PROGRESS_BAR_LEVELS
from utils.globs import PathFormat, format_path


class ImageFileWrapper:
    def __init__(self, image: Image = None, path: str = None):
        self.image = image
        self.path = path


def hash_image(
        image: Image,
        method: HashingMethod,
        hash_size: int = DEFAULT_HASH_SIZE
) -> str:
    if method == HashingMethod.HIST:
        hash_value = imagehash.dhash(image, hash_size=hash_size).__str__()
        hash_value += average_histogram_hash(image).__str__()
        return hash_value

    elif method == HashingMethod.BW:
        return imagehash.dhash(image, hash_size=hash_size).__str__()

    elif method == HashingMethod.RGB:
        im = image if image.mode == 'RGB' else image.convert('RGB')
        hash_value = imagehash.phash(im.getchannel('R'), hash_size=int(hash_size / 3)).__str__()
        hash_value += imagehash.phash(im.getchannel('G'), hash_size=int(hash_size / 3)).__str__()
        hash_value += imagehash.phash(im.getchannel('B'), hash_size=int(hash_size / 3)).__str__()
        return hash_value

    elif method == HashingMethod.RGBA:
        im = image if image.mode == 'RGBA' else image.convert('RGBA')
        hash_value = imagehash.phash(im.getchannel('R'), hash_size=int(hash_size / 4)).__str__()
        hash_value += imagehash.phash(im.getchannel('G'), hash_size=int(hash_size / 4)).__str__()
        hash_value += imagehash.phash(im.getchannel('B'), hash_size=int(hash_size / 4)).__str__()
        hash_value += imagehash.phash(im.getchannel('A'), hash_size=int(hash_size / 4)).__str__()
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


def report_info(
        img_paths: list[str],
        verbose: int = 0,
        progress_bar: int = PROGRESS_BAR_LEVELS[2],
        output_path_format: PathFormat = PathFormat.DIR_RELATIVE,
        root_dir: str = None
) -> None:
    print(f'To be implemented')  # TODO: Implement this


def calc_hash_size(
        img_paths: list[str],
        auto_hash_size: AutoHashSize = AutoHashSize.MAX_AVG_DIM,
        verbose: int = 0,
        progress_bar: int = PROGRESS_BAR_LEVELS[2],
        output_path_format: PathFormat = PathFormat.DIR_RELATIVE,
        root_dir: str = None
) -> tuple[int, list[str]]:
    pbar = None
    if verbose > 0:
        if progress_bar == PROGRESS_BAR_LEVELS[1]:
            pbar = tqdm(
                total=len(img_paths),
                desc='Determining hash size',
                bar_format='{desc}: {percentage:3.0f}% {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]',
                file=sys.stdout, leave=False
            )
        elif progress_bar == PROGRESS_BAR_LEVELS[2]:
            pbar = tqdm(total=len(img_paths), desc='Determining hash size', file=sys.stdout, leave=False)
        elif progress_bar not in PROGRESS_BAR_LEVELS:
            raise ValueError('Invalid progress bar level')
    if progress_bar == PROGRESS_BAR_LEVELS[0]:
        print('Determining hash size...', end='\n' if verbose > 1 else '', flush=True)

    has_errors = False
    max_hash_size = 0
    dims_total = 0
    im_count = 0
    new_img_paths = []
    for img_path in img_paths:
        if pbar is not None:
            pbar.update()

        im = None
        try:
            im = Image.open(img_path)
            im.verify()
            im = Image.open(img_path)

            if auto_hash_size == AutoHashSize.MAX_DIM:
                max_hash_size = max([max_hash_size, im.width, im.height])
            elif auto_hash_size == AutoHashSize.MAX_AVG_DIM:
                max_hash_size = max([max_hash_size, int((im.width + im.height) / 2)])
            elif auto_hash_size == AutoHashSize.AVG_DIM:
                dims_total += im.width + im.height
                im_count += 1
            elif auto_hash_size == AutoHashSize.AVG_AVG_DIM:
                dims_total += int((im.width + im.height) / 2)
                im_count += 1
            else:
                raise ValueError('Invalid AutoHashSize value')

            im.close()
            new_img_paths.append(img_path)
        except (
                ValueError, TypeError,
                Image.DecompressionBombError,
                OSError, EOFError, PermissionError,
                MemoryError
        ) as error:
            has_errors = True
            loop_errprint(
                f"Error reading '{format_path(img_path, output_path_format, root_dir)}': "
                f'{error.__str__()}. '
                f'File skipped.',
                pbar=pbar
            )
            if im is not None:
                im.close()
            continue

    if pbar is not None:
        pbar.close()

    if auto_hash_size == AutoHashSize.AVG_DIM:
        hash_size = int(dims_total / (im_count * 2))
    elif auto_hash_size == AutoHashSize.AVG_AVG_DIM:
        hash_size = int(dims_total / im_count * 2)
    else:
        hash_size = max_hash_size

    if verbose > 0:
        print(
            f'{"Determining hash size..." if progress_bar != PROGRESS_BAR_LEVELS[0] else ""}'
            f'{"" if (verbose > 1 and progress_bar == PROGRESS_BAR_LEVELS[0]) or has_errors else " "}'
            f'Calculated hash size: {colored(str(hash_size), attrs=["bold"])} '
            f'{colored("[DONE]", color="green", attrs=["bold"])}',
            flush=True
        )

    return hash_size, new_img_paths
