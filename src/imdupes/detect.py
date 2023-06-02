import os

import imagehash
from PIL import Image
from tqdm.auto import tqdm

from utils.globs import PathFormat


def detect(
        img_paths: list[str],
        console_output: bool = True,
        output_path_format: PathFormat = PathFormat.DIR_RELATIVE,
        progress_bar: bool = True,
        verbose: bool = False,
) -> list[str]:
    image_hashes = {}
    with tqdm(total=len(os.listdir()), desc='Finding identical images', position=0, leave=True) as pbar:
        for i, img_path in img_paths:
            pbar.update()
            with Image.open(img_path) as im:
                image_hash = imagehash.average_hash(im, hash_size=8)
                if image_hash in image_hashes:
                    image_hashes[image_hash].append(img_path)
                else:
                    image_hashes[image_hash] = [img_path]

    # Remove hashes with a single path
    duplicated_image_hashes = {hash_val: paths for hash_val, paths in image_hashes.items() if len(paths) > 1}

    duplicated_images_paths = []
    for paths in duplicated_image_hashes.values():
        for i, path in enumerate(paths):
            duplicated_images_paths.append(path)

    return duplicated_images_paths
