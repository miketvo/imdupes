import os
from enum import Enum
from os import path


class PathFormat(Enum):
    ABSOLUTE = 'absolute'
    PROG_RELATIVE = 'prog-relative'
    DIR_RELATIVE = 'dir-relative'
    FILENAME = 'filename'


def format_path(p: str, path_format: PathFormat, curdir: str = None) -> str:
    if path_format == PathFormat.ABSOLUTE:
        return path.abspath(p)
    if path_format == PathFormat.PROG_RELATIVE:
        return path.relpath(p)
    if path_format == PathFormat.DIR_RELATIVE:
        if curdir is None:
            raise ValueError(f'globs.format_path(): {PathFormat.DIR_RELATIVE.value} requires that currdir is provided.')
        return path.relpath(p, start=curdir)
    if path_format == PathFormat.FILENAME:
        return path.basename(p)


SUPPORTED_FILE_EXTS = [  # Refer to: https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html
    'blp',
    'bmp', 'dib',
    'dds',
    'eps',
    'gif',
    'icns', 'ico',
    'im',
    'jpg', 'jpeg', 'jpe', 'jfif', 'jif',
    'pcx',
    'png',
    'pbm', 'pgm', 'ppm', 'pnm',
    'sgi',
    'spi',
    'tga'
    'tif', 'tiff',
    'webp',
    'xbm',
]

INTERACTIVE_OPTS = {
    'y': 'Yes',
    'n': 'No',
    'x': 'Cancel and Exit',
}
