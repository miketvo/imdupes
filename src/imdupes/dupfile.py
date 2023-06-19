import os.path
from sys import exit
import re
import json
from PIL import Image
from termcolor import cprint, colored

from utils.globs import PathFormat, format_path
from utils.imutils import ImageFileWrapper


def save(
        dups: list[list[ImageFileWrapper]],
        file: str,
        verbose: int = 0
) -> None:
    try:
        f = open(file, 'wt')
        data = [[format_path(img.path, PathFormat.ABSOLUTE) for img in dup_imgs] for dup_imgs in dups]
        json.dump(data, f, indent=2)
        f.close()
    except (
            ValueError,
            OSError, EOFError, PermissionError,
            MemoryError
    ) as error:
        cprint(f"Error writing file '{file}': {error.__str__()}\nProgram terminated.", 'red')
        exit()

    if verbose > 0:
        cprint(f'Output saved to "{file}"', 'blue', attrs=['bold'])


def load(
        file: str,
        exclude: str = None,
        verbose: int = 0
) -> list[list[ImageFileWrapper]]:
    dups = []
    exclude_pattern = None if exclude is None else re.compile(exclude)
    excluded_count = 0
    has_err = False

    if verbose > 0:
        print(f'Reading "{file}"...', end='', flush=True)

    try:
        f = open(file, 'rt', errors='backslashreplace')
        data = json.load(f)
        f.close()
        for duplication in data:
            curr_dups = []
            for file_path in duplication:
                if not os.path.exists(file_path):
                    if not has_err:
                        has_err = True
                        if (verbose == 1) or (verbose > 1 and excluded_count == 0):
                            print()
                    if verbose > 0:
                        print(
                            f'"{file_path}" does not exist, entry skipped.',
                            flush=True
                        )
                    continue
                if not os.path.isfile(file_path):
                    cprint(
                        f'Error reading file "{file}": '
                        f'"{file_path}" is not a file\nProgram terminated.',
                        'red'
                    )
                    exit()
                if not os.path.isabs(file_path):
                    cprint(
                        f'Error reading file "{file}": '
                        f'Malformed entry: File path "{file_path}" must be absolute\nProgram terminated.',
                        'red'
                    )
                    exit()

                if exclude_pattern is not None and exclude_pattern.search(file_path) is not None:
                    if not has_err and excluded_count == 0 and verbose > 1:
                        print()
                    excluded_count += 1
                    if verbose > 1:
                        print(f'Excluded entry: "{file_path}"')
                    continue

                im = None
                try:
                    im = Image.open(file_path)
                    im.verify()
                    im = Image.open(file_path)

                    if im.format == 'PNG' and im.mode != 'RGBA':
                        im = im.convert('RGBA')

                    curr_dups.append(ImageFileWrapper(im, file_path))

                    im.close()
                except (
                        ValueError, TypeError,
                        Image.DecompressionBombError,
                        OSError, EOFError, PermissionError,
                        MemoryError
                ) as error:
                    print(
                        f"Error scanning '{file_path}': "
                        f'{error.__str__()}. '
                        f'File skipped.',
                        flush=True
                    )
                    if im is not None:
                        im.close()
                    continue

            # Skip all duplication groups with length < 2, which can happen if all files within them are excluded, or
            # are skipped because of error when loading the image file
            if len(curr_dups) > 1:
                dups.append(curr_dups)

    except (
            ValueError,
            OSError, EOFError, PermissionError,
            MemoryError
    ) as error:
        cprint(f"Error reading file '{file}': {error.__str__()}\nProgram terminated.", 'red')
        exit()

    # Sort duplications in order of decreasing resolution (width * height) so that the highest resolution image is kept
    # during cleaning step
    for i in range(len(dups)):
        dups[i] = sorted(
            dups[i],
            key=lambda img: img.image.size[0] * img.image.size[1],
            reverse=True
        )

    if excluded_count == 0 and verbose > 1:
        cprint(f'{"" if has_err else " "}No file(s) excluded. ', 'yellow', end='')

    if verbose > 0:
        print(
            f'{"" if (verbose > 1) or (verbose > 1 and excluded_count > 0) or (verbose > 0 and has_err) else " "}'
            f'Loaded {colored(str(len(dups)), attrs=["bold"])} duplication(s) '
            f'across {colored(str(sum(len(lst) for lst in dups)), attrs=["bold"])} file(s) '
            f'{colored("[DONE]", color="green", attrs=["bold"])}',
            flush=True
        )

    return dups
