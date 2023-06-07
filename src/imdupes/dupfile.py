from utils.imutils import ImageFileWrapper


def load(
        file: str,
        exclude: str = None,
        verbose: int = 0
) -> list[list[ImageFileWrapper]]:
    dup_imgs = []

    try:
        with open(file, 'rt') as f:
            pass
    except (
            ValueError, TypeError,
            OSError, EOFError, PermissionError,
            MemoryError
    ) as error:
        pass

    return dup_imgs
