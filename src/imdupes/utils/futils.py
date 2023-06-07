from sys import exit
import os
import re
from termcolor import cprint, colored

from utils.globs import SUPPORTED_FILE_EXTS
from utils.globs import INTERACTIVE_OPTS
from utils.globs import PathFormat, format_path
from utils.imutils import ImageFileWrapper


# noinspection DuplicatedCode
def index_images(
        directory: str,
        exclude: str = None,
        recursive: bool = False,
        verbose: int = 0,
        output_path_format: PathFormat = PathFormat.DIR_RELATIVE
) -> list[str]:
    img_paths = []
    abs_root = os.path.abspath(directory)
    exclude_pattern = None if exclude is None else re.compile(exclude)

    if verbose > 0:
        print('Indexing images...', flush=True)

    if recursive:
        for root, dirs, files in os.walk(abs_root):
            for file in files:
                file_path = os.path.join(root, file)
                file_name = os.path.basename(file_path)
                if exclude_pattern is not None and exclude_pattern.search(file_name) is not None:
                    if verbose > 1:
                        print(f'Excluded file: "{format_path(file_path, output_path_format, directory)}"')
                    continue

                file_extension = os.path.splitext(file)[1].lower()[1:]
                if file_extension in SUPPORTED_FILE_EXTS:
                    img_paths.append(file_path)
    else:
        for file in os.listdir(abs_root):
            file_path = os.path.join(abs_root, file)
            if os.path.isfile(file_path):
                file_name = os.path.basename(file_path)
                if exclude_pattern is not None and exclude_pattern.search(file_name) is not None:
                    if verbose > 1:
                        print(f'Excluded file: "{format_path(file_path, output_path_format, directory)}"')
                    continue

                file_extension = os.path.splitext(file)[1].lower()[1:]
                if file_extension in SUPPORTED_FILE_EXTS:
                    img_paths.append(file_path)

    if len(img_paths) == 0:
        cprint(f'"{directory}" has no valid image files. Program terminated.', 'red')
        exit()

    if verbose > 0:
        print(
            f'Found {colored(str(len(img_paths)), attrs=["bold"])} image(s) '
            f'{colored("[DONE]", color="green", attrs=["bold"])}',
            flush=True
        )

    return img_paths


def clean(
        hashed_dups: dict[str, list[ImageFileWrapper]],
        root_dir: str = None,
        interactive: bool = False,
        verbose: int = 0,
        output_path_format: PathFormat = PathFormat.DIR_RELATIVE
) -> None:
    if len(hashed_dups) == 0:
        print(f'No duplications to clean', flush=True)
        return

    if verbose > 0:
        print(f'\nCleaning duplications...', flush=True)

    for dup_imgs_index, dup_imgs in enumerate(hashed_dups.items(), start=1):
        if interactive:
            print(colored(f'\n[ DUPLICATION {dup_imgs_index}/{len(hashed_dups)} ]', 'magenta', attrs=['bold']))
            for dup_img_index, dup_img in enumerate(dup_imgs[1], start=1):
                while True:
                    choices = '\n    '.join(f'[{key.upper()}] {value}' for key, value in INTERACTIVE_OPTS.items())
                    choice = input(
                        f'{colored(f"Image {dup_img_index}/{len(dup_imgs[1])}:", "yellow")} Delete '
                        f'"{format_path(dup_img.path, output_path_format, root_dir)}"?\n'
                        f'    {colored(choices)}\n{colored(">>", "yellow", attrs=["bold"])} '
                    ).lower()

                    if choice in INTERACTIVE_OPTS.keys():
                        if choice == 'y':
                            try:
                                os.remove(dup_img.path)
                                if verbose > 0:
                                    print(f'-- Deleted "{format_path(dup_img.path, output_path_format, root_dir)}"')
                            except (OSError, PermissionError) as error:
                                cprint(
                                    f'Error deleting file '
                                    f'"{format_path(dup_img.path, output_path_format, root_dir)}": {str(error)}',
                                    'red'
                                )
                        if choice == 'x':
                            cprint('Cleaning cancelled', 'red')
                            return

                        break

                    else:
                        print('Invalid choice. Please choose a valid option.')

        else:
            for dup_index in range(1, len(dup_imgs[1])):
                try:
                    os.remove(dup_imgs[1][dup_index].path)
                    if verbose > 0:
                        print(
                            f'-- Deleted "{format_path(dup_imgs[1][dup_index].path, output_path_format, root_dir)}"',
                            flush=True
                        )
                except (OSError, PermissionError) as error:
                    cprint(
                        f'Error deleting file '
                        f'"{format_path(dup_imgs[1][dup_index].path, output_path_format, root_dir)}": {str(error)}',
                        'red'
                    )

    if verbose > 0:
        if interactive:
            print()
        print(f'{colored("[DONE]", color="green", attrs=["bold"])}', flush=True)
