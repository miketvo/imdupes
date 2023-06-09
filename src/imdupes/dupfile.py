import os.path
from sys import exit
import re
import json
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

    if verbose > 0:
        print(f'Reading "{file}"...', flush=True)

    try:
        f = open(file, 'rt', errors='backslashreplace')
        data = json.load(f)
        f.close()
        for duplication in data:
            curr_dups = []
            for file_path in duplication:
                if not os.path.exists(file_path):
                    cprint(
                        f'Error reading file "{file}": '
                        f'Malformed entry: Incorrect path "{file_path}"\nProgram terminated.',
                        'red'
                    )
                    exit()
                if not os.path.isfile(file_path):
                    cprint(
                        f'Error reading file "{file}": '
                        f'Malformed entry: "{file_path}" is not a file\nProgram terminated.',
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
                    if verbose > 1:
                        print(f'Excluded file: "{file_path}"')
                    continue
                curr_dups.append(ImageFileWrapper(path=file_path))

            # Skip all empty duplication groups, which can happen if all files within them are excluded
            if len(curr_dups) > 0:
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

    if verbose > 0:
        print(
            f'Loaded {colored(str(len(dups)), attrs=["bold"])} duplication(s) '
            f'across {colored(str(sum(len(lst) for lst in dups)), attrs=["bold"])} file(s) '
            f'{colored("[DONE]", color="green", attrs=["bold"])}',
            flush=True
        )

    return dups
