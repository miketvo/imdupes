import os
import re
from termcolor import cprint, colored

from utils.globs import SUPPORTED_FILE_EXTS, PathFormat, format_path


def index_images(
        directory: str,
        exclude: str = None,
        recursive: bool = False,
        verbose: bool = False,
        output_path_format: PathFormat = PathFormat.DIR_RELATIVE
) -> list[str]:
    img_paths = []
    abs_root = os.path.abspath(directory)
    exclude_pattern = None if exclude is None else re.compile(exclude)

    if verbose:
        print('Indexing images...', end='')

    if recursive:
        for root, dirs, files in os.walk(abs_root):
            for file in files:
                file_path = os.path.join(root, file)
                file_name = os.path.basename(file_path)
                if exclude_pattern is not None and exclude_pattern.search(file_name):
                    continue

                file_extension = os.path.splitext(file)[1].lower()
                if file_extension in SUPPORTED_FILE_EXTS:
                    img_paths.append(file_path)
    else:
        for file in os.listdir(abs_root):
            file_path = os.path.join(abs_root, file)
            if os.path.isfile(file_path):
                file_name = os.path.basename(file_path)
                if exclude_pattern is not None and exclude_pattern.search(file_name):
                    continue

                file_extension = os.path.splitext(file)[1].lower()
                if file_extension in SUPPORTED_FILE_EXTS:
                    img_paths.append(file_path)

    if len(img_paths) == 0:
        cprint(f' "{directory}" has no valid image files. Program terminated.', 'red')
        exit()

    if verbose:
        print(
            f' Found {colored(str(len(img_paths)), attrs=["bold"])} image(s) '
            f'{colored("[DONE]", color="green", attrs=["bold"])}'
        )

    return img_paths


def clean(
        img_paths: list[str],
        interactive: bool = False,
        progress_bar: bool = True,
        verbose: bool = False,
        output_path_format: PathFormat = PathFormat.DIR_RELATIVE
) -> None:
    pass
