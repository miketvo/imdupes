import warnings
import PIL.Image
import imagehash
from PIL import Image
from tqdm.auto import tqdm
from termcolor import cprint, colored

from utils.globs import PathFormat, format_path


PIL.Image.MAX_IMAGE_PIXELS = 846_071_539_488  # Kuala Lumpur 846 gigapixels: https://www.panaxity.com/
warnings.simplefilter('ignore', Image.DecompressionBombWarning)


def detect(
        img_paths: list[str],
        root_dir: str = None,
        console_output: bool = True,
        output_path_format: PathFormat = PathFormat.DIR_RELATIVE,
        verbose: bool = False
) -> dict[imagehash.ImageHash, list[str]]:
    image_hashes = {}

    if verbose:
        with tqdm(total=len(img_paths), desc='Scanning for identical images', position=0, leave=False) as pbar:
            for img_path in img_paths:
                pbar.update()

                try:
                    im = Image.open(img_path)
                except (ValueError, TypeError, Image.DecompressionBombError, OSError, EOFError) as error:
                    cprint(
                        f'Error reading {format_path(img_path, output_path_format, root_dir)}: '
                        f'{error.__str__()}. '
                        f'File skipped.',
                        'red'
                    )
                    continue

                image_hash = imagehash.average_hash(im, hash_size=8)
                if image_hash in image_hashes:
                    image_hashes[image_hash].append(img_path)
                else:
                    image_hashes[image_hash] = [img_path]

    else:
        for img_path in img_paths:
            try:
                im = Image.open(img_path)
            except (ValueError, TypeError, Image.DecompressionBombError, OSError, EOFError) as error:
                cprint(
                    f'Error reading {format_path(img_path, output_path_format, root_dir)}: '
                    f'{error.__str__()}. '
                    f'File skipped.',
                    'red'
                )
                continue

            image_hash = imagehash.average_hash(im, hash_size=8)
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
            end=''
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
