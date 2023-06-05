__version__ = '0.1.1-beta'
__app_name__ = 'imdupes'
__prog_desc__ = \
    'Quickly detects and removes identical images. Has two modes:\n' \
    "\t- 'detect' console prints the detected identical image paths/filenames\n" \
    "\t- 'clean' removes the detected identical images, keeping only the first copy\n" \
    'Warning: Deleted files are not recoverable, proceed with caution'
__prog_epilog__ = \
    'Note: This program ignores any non-image file in the target directory\n\n' \
    '*: Smaller hash sizes are better for detecting visually similar images, while larger hash sizes are\n' \
    '   better for identifying identical images; The smaller the hash size, the better the performance\n' \
    '\n' \
    '   Smallest accepted hash size is 8\n' \
    '\n' \
    'Algorithm: Average Hash (https://www.hackerfactor.com/blog/index.php?/archives/432-Looks-Like-It.html)'
