import os.path
from sys import exit
import re
from termcolor import cprint, colored

from utils.imutils import ImageFileWrapper


def load(
        file: str,
        exclude: str = None,
        verbose: int = 0
) -> list[list[ImageFileWrapper]]:
    dup_imgs = []

    if verbose > 0:
        print(f'Reading "{file}"...', flush=True)

    try:
        with open(file, 'rt', errors='backslashreplace') as f:
            curr_dups = None
            curr_dups_num = 0
            dup_header_pattern = re.compile('\\[ DUPLICATION [0-9]+ ]')
            exclude_pattern = None if exclude is None else re.compile(exclude)

            for line_num, line in enumerate(f, start=1):
                stripped_line = line.strip()

                if curr_dups is None:
                    if dup_header_pattern.fullmatch(stripped_line):
                        curr_dups_num += 1
                        if stripped_line != f'[ DUPLICATION {curr_dups_num} ]':
                            cprint(
                                f'Error reading file "{file}", line {line_num}: '
                                f'Incorrect duplication numbering\nProgram terminated.',
                                'red'
                            )
                            exit()
                        curr_dups = []
                    else:
                        cprint(
                            f'Error reading file "{file}", line {line_num}: '
                            f'Malformed duplication header\nProgram terminated.',
                            'red'
                        )
                        exit()

                else:
                    if len(stripped_line) == 0:
                        dup_imgs.append(curr_dups)
                        curr_dups = []

                    file_path = stripped_line
                    if not os.path.isabs(file_path):
                        cprint(
                            f'Error reading file "{file}", line {line_num}: '
                            f'Malformed entry: File path "{file_path}" must be absolute\nProgram terminated.',
                            'red'
                        )
                        exit()
                    if not os.path.exists(file_path):
                        cprint(
                            f'Error reading file "{file}", line {line_num}: '
                            f'Malformed entry: Incorrect path "{file_path}"\nProgram terminated.',
                            'red'
                        )
                        exit()
                    if not os.path.isfile(file_path):
                        cprint(
                            f'Error reading file "{file}", line {line_num}: '
                            f'Malformed entry: "{file_path}" is not a file\nProgram terminated.',
                            'red'
                        )
                        exit()

                    if exclude_pattern is not None and exclude_pattern.search(file_path) is not None:
                        if verbose > 1:
                            print(f'Excluded file: "{file_path}"')
                        continue
                    curr_dups.append(ImageFileWrapper(path=file_path))

            if curr_dups is not None:
                dup_imgs.append(curr_dups)

    except (
            ValueError,
            OSError, EOFError, PermissionError,
            MemoryError
    ) as error:
        cprint(f"Error reading file '{file}': {error.__str__()}\nProgram terminated.", 'red')
        exit()

    if verbose > 0:
        print(
            f'Loaded {colored(str(len(dup_imgs)), attrs=["bold"])} duplication(s) '
            f'across {colored(str(sum(len(lst) for lst in dup_imgs)), attrs=["bold"])} file(s) '
            f'{colored("[DONE]", color="green", attrs=["bold"])}',
            flush=True
        )

    return dup_imgs
