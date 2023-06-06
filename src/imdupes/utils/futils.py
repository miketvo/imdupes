from typing import TextIO
import sys
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
        verbose: int = 0
) -> list[str]:
    img_paths = []
    abs_root = os.path.abspath(directory)
    exclude_pattern = None if exclude is None else re.compile(exclude)

    if verbose > 0:
        print('Indexing images...', end='', flush=True)

    if recursive:
        for root, dirs, files in os.walk(abs_root):
            for file in files:
                file_path = os.path.join(root, file)
                file_name = os.path.basename(file_path)
                if exclude_pattern is not None and exclude_pattern.search(file_name) is not None:
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
                    continue

                file_extension = os.path.splitext(file)[1].lower()[1:]
                if file_extension in SUPPORTED_FILE_EXTS:
                    img_paths.append(file_path)

    if len(img_paths) == 0:
        cprint(f' "{directory}" has no valid image files. Program terminated.', 'red')
        exit()

    if verbose > 0:
        print(
            f' Found {colored(str(len(img_paths)), attrs=["bold"])} image(s) '
            f'{colored("[DONE]", color="green", attrs=["bold"])}',
            flush=True
        )

    return img_paths


def print_dups(
        hashed_dups: dict[str, list[ImageFileWrapper]],
        root_dir: str = None,
        output_path_format: PathFormat = PathFormat.DIR_RELATIVE,
        colored_cluster_header: bool = False,
        show_hash_cluster_header: bool = False,
        file: TextIO = sys.stdout,
        flush: bool = False
) -> None:
    for i, dup_imgs in enumerate(hashed_dups.items(), start=1):
        hash_str = dup_imgs[0][:127] + '...' + dup_imgs[0][-127:] if len(dup_imgs[0]) > 256 else dup_imgs[0]
        hash_str_print = f' | hash: {hash_str}' if show_hash_cluster_header else ''
        print(
            colored(f'[ DUPLICATION {i}{hash_str_print} ]', 'blue', attrs=['bold']) if colored_cluster_header
            else f'[ DUPLICATION {i}{hash_str_print} ]',
            file=file
        )

        for dup_img in dup_imgs[1]:
            print(format_path(dup_img.path, output_path_format, root_dir), file=file)
        print(file=file, flush=flush)


def clean(
        hashed_dups: dict[str, list[ImageFileWrapper]],
        root_dir: str = None,
        interactive: bool = False,
        verbose: int = 0,
        output_path_format: PathFormat = PathFormat.DIR_RELATIVE
) -> None:
    if verbose > 0:
        print(f'\nCleaning duplications...', flush=True)

    for dup_imgs in hashed_dups.values():
        if interactive:
            for dup_img in dup_imgs:
                while True:
                    choices = '\n\t'.join(f'[{key.upper()}] {value}' for key, value in INTERACTIVE_OPTS.items())
                    choice = input(
                        f'Delete "{format_path(dup_img.path, output_path_format, root_dir)}"?\n\t'
                        f'{colored(choices)}\n{colored(">>", "yellow", attrs=["bold"])} '
                    ).lower()

                    if choice in INTERACTIVE_OPTS.keys():
                        if choice == 'y':
                            try:
                                os.remove(dup_img.path)
                                if verbose > 0:
                                    print(f'-- Deleted "{format_path(dup_img.path, output_path_format, root_dir)}"')
                            except OSError as e:
                                cprint(
                                    f'Error deleting file '
                                    f'"{format_path(dup_img.path, output_path_format, root_dir)}": {str(e)}',
                                    'red'
                                )
                        if choice == 'x':
                            cprint('Cleaning cancelled. Program terminated.', 'red')
                            exit()

                        break

                    else:
                        print('Invalid choice. Please choose a valid option.')

        else:
            for i in range(1, len(dup_imgs)):
                try:
                    os.remove(dup_imgs[i].path)
                    if verbose > 0:
                        print(f'-- Deleted "{format_path(dup_imgs[i].path, output_path_format, root_dir)}"', flush=True)
                except OSError as e:
                    cprint(
                        f'Error deleting file "{format_path(dup_imgs[i].path, output_path_format, root_dir)}": '
                        f'{str(e)}',
                        'red'
                    )

    if verbose > 0:
        print(f'{colored("[DONE]", color="green", attrs=["bold"])}', flush=True)
