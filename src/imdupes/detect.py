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


def detect(
        img_paths: list[str],
        hash_size: int = DEFAULT_HASH_SIZE,
        root_dir: str = None,
        console_output: bool = True,
        output_path_format: PathFormat = PathFormat.DIR_RELATIVE,
        verbose: int = 0
) -> dict[str, list[ImageFileWrapper]]:
    hashed_images: dict[str, list[ImageFileWrapper]] = {}

    # Image hashing
    pbar = None
    if verbose > 0:
        pbar = tqdm(total=len(img_paths), desc='Scanning for identical images', position=0, leave=False)
    for img_path in img_paths:
        if pbar is not None:
            pbar.update()

        try:
            im = Image.open(img_path)
            if im.format == 'PNG' and im.mode != 'RGBA':
                im = im.convert('RGBA')

        except (ValueError, TypeError, Image.DecompressionBombError, OSError, EOFError) as error:
            if pbar is not None:
                pbar.write(
                    f"Error reading '{format_path(img_path, output_path_format, root_dir)}': "
                    f'{error.__str__()}. '
                    f'File skipped.'
                )
            else:
                print(
                    f"Error reading '{format_path(img_path, output_path_format, root_dir)}': "
                    f'{error.__str__()}. '
                    f'File skipped.',
                    flush=True
                )
            continue

        image_hash = imagehash.average_hash(im, hash_size=hash_size).__str__()
        if image_hash in hashed_images:
            hashed_images[image_hash].append(ImageFileWrapper(im, img_path))
        else:
            hashed_images[image_hash] = [ImageFileWrapper(im, img_path)]

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

    # Output
    if verbose > 0:
        print(
            f'Scanning for identical images... '
            f'Found {colored(str(len(hashed_dups.values())), attrs=["bold"])} duplication(s) '
            f'across {colored(str(sum(len(lst) for lst in hashed_dups.values())), attrs=["bold"])} file(s) '
            f'{colored("[DONE]", color="green", attrs=["bold"])}',
            end='',
            flush=True
        )

    if console_output:
        if verbose > 0:
            print(':')
        for dup_imgs in hashed_dups.values():
            print()
            for dup_img in dup_imgs:
                print(format_path(dup_img.path, output_path_format, root_dir))
    else:
        print()

    return hashed_dups
