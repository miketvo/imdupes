import sys
from typing import TextIO
from termcolor import colored
from utils.imutils import ImageFileWrapper
from utils.globs import PathFormat, format_path


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
        hash_str = dup_imgs[0][:48] + '...' if len(dup_imgs[0]) > 48 else dup_imgs[0]
        hash_str_print = f' | hash: {hash_str}' if show_hash_cluster_header else ''
        print(
            colored(f'[ DUPLICATION {i}{hash_str_print} ]', 'magenta', attrs=['bold']) if colored_cluster_header
            else f'[ DUPLICATION {i}{hash_str_print} ]',
            file=file
        )

        for dup_img in dup_imgs[1]:
            print(format_path(dup_img.path, output_path_format, root_dir), file=file)
        print(file=file, flush=flush)
