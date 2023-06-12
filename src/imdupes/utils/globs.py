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
        return path.relpath(p, start=curdir)
    if path_format == PathFormat.FILENAME:
        return path.basename(p)


SUPPORTED_FILE_EXTS = [  # Refer to: https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html

    # Fully supported read/write extensions
    'blp',
    'bmp', 'dib',
    'dds',
    'eps',  # User needs Ghostscript for Pillow to be able to read this format: https://www.ghostscript.com/
    'gif',
    'icns', 'ico',
    'im',
    'jpg', 'jpeg', 'jpe', 'jfif', 'jif',
    'jp2', 'j2k', 'jpf', 'jpm', 'jpg2', 'j2c', 'jpc', 'jpx', 'mj2',
    'pcx',
    'png',
    'pbm', 'pgm', 'ppm', 'pnm',
    'sgi',
    'spi',
    'tga'
    'tif', 'tiff',
    'webp',
    'xbm',

    # Limited read-only extensions
    'cur',
    'fits', 'fit', 'fts',
    'mpo',
    'pxr',
    'psd',
    'ras', 'sun',
    'xpm',
]
DUPFILE_EXT = 'imdup'

INTERACTIVE_OPTS = {
    'y': 'Yes',
    'n': 'No',
    'x': 'Cancel and Exit',
}


class HashingMethod(Enum):
    RGBA = 'rgba-hashing'
    RGB = 'rgb-hashing'
    BW = 'grayscale-hashing'


DEFAULT_HASH_SIZE = 512

VERBOSE_LEVELS = [1, 2]
PROGRESS_BAR_LEVELS = [0, 1, 2]
