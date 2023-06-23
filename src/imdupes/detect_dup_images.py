import sys
from sys import exit
import warnings
from PIL import Image
from tqdm.auto import tqdm
from termcolor import colored

from utils import loop_errprint
from utils.globs import PathFormat, format_path
from utils.globs import HashingMethod
from utils.globs import DEFAULT_HASH_SIZE
from utils.imutils import hash_image, ImageFileWrapper
from utils.globs import PROGRESS_BAR_LEVELS


Image.MAX_IMAGE_PIXELS = 846_071_539_488  # Kuala Lumpur 846 gigapixels: https://www.panaxity.com/
warnings.simplefilter('ignore', Image.DecompressionBombWarning)


def detect_dup_images(
        img_paths: list[str],
        method: HashingMethod,
        hash_size: int = DEFAULT_HASH_SIZE,
        root_dir: str = None,
        output_path_format: PathFormat = PathFormat.DIR_RELATIVE,
        verbose: int = 0,
        progress_bar: int = PROGRESS_BAR_LEVELS[2]
) -> dict[str, list[ImageFileWrapper]]:
    try:
        hashed_images: dict[str, list[ImageFileWrapper]] = {}
        has_errors = False

        # Image hashing
        pbar = None
        if verbose > 0:
            if progress_bar == PROGRESS_BAR_LEVELS[1]:
                pbar = tqdm(
                    total=len(img_paths),
                    desc='Scanning for identical images',
                    bar_format='{desc}: {percentage:3.0f}% {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]',
                    file=sys.stdout, leave=False
                )
            elif progress_bar == PROGRESS_BAR_LEVELS[2]:
                pbar = tqdm(total=len(img_paths), desc='Scanning for identical images', file=sys.stdout, leave=False)
            else:
                raise ValueError('Invalid progress bar level')
        if progress_bar == PROGRESS_BAR_LEVELS[0]:
            print(
                'Scanning for identical images...', end='\n' if verbose > 1 else '', flush=True
            )
        for img_path in img_paths:
            if pbar is not None:
                pbar.update()

            if verbose > 1:
                if progress_bar == PROGRESS_BAR_LEVELS[0]:
                    print(f'Scanning "{format_path(img_path, output_path_format, root_dir)}"')
                else:
                    pbar.write(f'Scanning "{format_path(img_path, output_path_format, root_dir)}"')

            im = None
            try:
                im = Image.open(img_path)
                im.verify()
                im = Image.open(img_path)

                if im.format == 'PNG' and im.mode != 'RGBA':
                    im = im.convert('RGBA')

                image_hash = hash_image(im, method=method, hash_size=hash_size)
                if image_hash in hashed_images:
                    hashed_images[image_hash].append(ImageFileWrapper(im, img_path))
                else:
                    hashed_images[image_hash] = [ImageFileWrapper(im, img_path)]

                im.close()

            except (
                    ValueError, TypeError,
                    Image.DecompressionBombError,
                    OSError, EOFError, PermissionError,
                    MemoryError
            ) as error:
                has_errors = True
                loop_errprint(
                    f"Error scanning '{format_path(img_path, output_path_format, root_dir)}': "
                    f'{error.__str__()}. '
                    f'File skipped.',
                    pbar=pbar
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
                f'{"Scanning for identical images..." if progress_bar != PROGRESS_BAR_LEVELS[0] else ""}'
                f'{"" if (verbose > 1 and progress_bar == PROGRESS_BAR_LEVELS[0]) or has_errors else " "}'
                f'Found {colored(str(len(hashed_dups.values())), attrs=["bold"])} duplication(s) '
                f'across {colored(str(sum(len(lst) for lst in hashed_dups.values())), attrs=["bold"])} file(s) '
                f'{colored("[DONE]", color="green", attrs=["bold"])}',
                flush=True
            )

        return hashed_dups
    except KeyboardInterrupt:
        if pbar is not None:
            pbar.close()
        exit()
