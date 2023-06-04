import warnings
import imagehash
from PIL import Image
from tqdm.auto import tqdm
from termcolor import colored

from utils.globs import PathFormat, format_path


Image.MAX_IMAGE_PIXELS = 846_071_539_488  # Kuala Lumpur 846 gigapixels: https://www.panaxity.com/
warnings.simplefilter('ignore', Image.DecompressionBombWarning)


def detect(
        img_paths: list[str],
        hash_size: int = 256,
        root_dir: str = None,
        console_output: bool = True,
        output_path_format: PathFormat = PathFormat.DIR_RELATIVE,
        verbose: bool = False
) -> dict[imagehash.ImageHash, list[str]]:
    image_hashes = {}

    pbar = None
    if verbose:
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
                    f'Error reading {format_path(img_path, output_path_format, root_dir)}: '
                    f'{error.__str__()}. '
                    f'File skipped.',
                    flush=True
                )
            continue

        image_hash = imagehash.average_hash(im, hash_size=hash_size).__str__()
        if image_hash in image_hashes:
            image_hashes[image_hash].append(img_path)
        else:
            image_hashes[image_hash] = [img_path]

    # Remove hashes with a single path
    duplicated_image_hashes = {hash_val: paths for hash_val, paths in image_hashes.items() if len(paths) > 1}

    if verbose:
        print(
            f'Scanning for identical images... '
            f'Found {colored(str(len(duplicated_image_hashes.values())), attrs=["bold"])} duplication(s) '
            f'across {colored(str(sum(len(lst) for lst in duplicated_image_hashes.values())), attrs=["bold"])} file(s) '
            f'{colored("[DONE]", color="green", attrs=["bold"])}',
            end='',
            flush=True
        )

    if console_output:
        if verbose:
            print(':')
        for paths in duplicated_image_hashes.values():
            print()
            for path in paths:
                print(format_path(path, output_path_format, root_dir))
    else:
        print()

    return duplicated_image_hashes
