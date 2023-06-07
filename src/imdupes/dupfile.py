from sys import exit
from termcolor import cprint

from utils.imutils import ImageFileWrapper


def load(
        file: str,
        exclude: str = None,
        verbose: int = 0
) -> list[list[ImageFileWrapper]]:
    dup_imgs = []

    try:
        with open(file, 'rt', errors='backslashreplace') as f:
            pass
    except (
            ValueError,
            OSError, EOFError, PermissionError,
            MemoryError
    ) as error:
        cprint(f"Error reading file '{file}': {error.__str__()}\nProgram terminated.", 'red')
        exit()

    return dup_imgs
