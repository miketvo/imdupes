import sys
import warnings
import imagehash
from PIL import Image
from tqdm.auto import tqdm
from termcolor import colored

from utils.globs import PathFormat, format_path
from utils.globs import DEFAULT_HASH_SIZE
from utils.imutils import ImageFileWrapper


Image.MAX_IMAGE_PIXELS = 846_071_539_488  # Kuala Lumpur 846 gigapixels: https://www.panaxity.com/
warnings.simplefilter('ignore', Image.DecompressionBombWarning)


def detect_dup_images(
        img_paths: list[str],
        hash_size: int = DEFAULT_HASH_SIZE,
        root_dir: str = None,
        output_path_format: PathFormat = PathFormat.DIR_RELATIVE,
        verbose: int = 0
) -> dict[str, list[ImageFileWrapper]]:
    hashed_images: dict[str, list[ImageFileWrapper]] = {}

    # Image hashing
    pbar = None
    if verbose > 0:
        pbar = tqdm(total=len(img_paths), desc='Scanning for identical images', file=sys.stdout, leave=False)
    for img_path in img_paths:
        if pbar is not None:
            pbar.update()

        if verbose > 1:
            if pbar is not None:
                pbar.write(f'Processing "{format_path(img_path, output_path_format, root_dir)}"')
            else:
                print(f'Processing "{format_path(img_path, output_path_format, root_dir)}"', flush=True)

        im = None
        try:
            im = Image.open(img_path)
            if im.format == 'PNG' and im.mode != 'RGBA':
                im = im.convert('RGBA')

            image_hash = imagehash.average_hash(im, hash_size=hash_size).__str__()
            if image_hash in hashed_images:
                hashed_images[image_hash].append(ImageFileWrapper(im, img_path))
            else:
                hashed_images[image_hash] = [ImageFileWrapper(im, img_path)]

        except (ValueError, TypeError, Image.DecompressionBombError, OSError, EOFError, MemoryError) as error:
            if pbar is not None:
                pbar.write(
                    f"Error hashing '{format_path(img_path, output_path_format, root_dir)}': "
                    f'{error.__str__()}. '
                    f'File skipped.'
                )
            else:
                print(
                    f"Error hashing '{format_path(img_path, output_path_format, root_dir)}': "
                    f'{error.__str__()}. '
                    f'File skipped.',
                    flush=True
                )
            if im is not None:
                im.close()
            continue

    if pbar is not None:
        pbar.close()

    # Remove hashes with a single path
    hashed_dups: dict[str, list[ImageFileWrapper]] = {
        hash_val: dup_imgs for hash_val, dup_imgs in hashed_images.items() if len(dup_imgs) > 1
    }

    # Sort duplications in order of decreasing resolution (width * height) so that the highest resolution image is kept
    # during cleaning step
    image_hashes = list(hashed_dups.keys())
    for i in range(len(image_hashes)):
        hashed_dups[image_hashes[i]] = sorted(
            hashed_dups[image_hashes[i]],
            key=lambda img: img.image.size[0] * img.image.size[1],
            reverse=True
        )

    if verbose > 0:
        print(
            f'Scanning for identical images... '
            f'Found {colored(str(len(hashed_dups.values())), attrs=["bold"])} duplication(s) '
            f'across {colored(str(sum(len(lst) for lst in hashed_dups.values())), attrs=["bold"])} file(s) '
            f'{colored("[DONE]", color="green", attrs=["bold"])}',
            flush=True
        )

    return hashed_dups
