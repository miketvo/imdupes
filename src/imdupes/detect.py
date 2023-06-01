from utils import PathFormat


def detect(
        directory: str,
        exclude: str = None,
        recursive: bool = False,
        output_format: PathFormat = PathFormat.ABSOLUTE,
        progress_bar: bool = True,
        verbose: bool = False
) -> list[str]:
    print(directory, exclude, recursive, output_format, progress_bar, verbose)

    return []
