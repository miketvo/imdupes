import imagehash
from PIL import Image
from tqdm.auto import tqdm
from termcolor import colored

from utils.globs import PathFormat, format_path


def detect(
        img_paths: list[str],
        console_output: bool = True,
        output_path_format: PathFormat = PathFormat.DIR_RELATIVE,
        root_dir: str = None,
        progress_bar: bool = True,
        verbose: bool = False,
) -> dict[str, str]:
    image_hashes = {}

    if verbose:
        print('Scanning for identical images...')

    if progress_bar:
        with tqdm(total=len(img_paths), position=0, leave=True) as pbar:
            for img_path in img_paths:
                pbar.update()
                with Image.open(img_path) as im:
                    image_hash = imagehash.average_hash(im, hash_size=8)
                    if image_hash in image_hashes:
                        image_hashes[image_hash].append(img_path)
                    else:
                        image_hashes[image_hash] = [img_path]
    else:
        for img_path in img_paths:
            with Image.open(img_path) as im:
                image_hash = imagehash.average_hash(im, hash_size=8)
                if image_hash in image_hashes:
                    image_hashes[image_hash].append(img_path)
                else:
                    image_hashes[image_hash] = [img_path]

    # Remove hashes with a single path
    duplicated_image_hashes = {hash_val: paths for hash_val, paths in image_hashes.items() if len(paths) > 1}

    if verbose:
        print(
            f'{colored("[DONE]", color="green", attrs=["bold"])} '
            f'Found {len(duplicated_image_hashes.values())} identical images',
            end=''
        )

    if console_output:
        print(':')
        for paths in duplicated_image_hashes.values():
            for path in paths:
                print(format_path(path, output_path_format, root_dir))
    else:
        print('.')

    return duplicated_image_hashes
