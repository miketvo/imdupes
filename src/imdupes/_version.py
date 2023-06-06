__version__ = '0.1.2-beta'
__app_name__ = 'imdupes'
__prog_usage__ = f'{__app_name__} {{scan,clean}} [OPTIONS] DIRECTORY'
__prog_desc__ = \
    'Quickly detects and removes identical images. Has two modes:\n' \
    "\t- 'scan' scans and console prints the detected identical image paths/filenames\n" \
    "\t- 'clean' scans and removes the detected identical images, keeping only the first copy\n" \
    'Warning: Deleted files are not recoverable, proceed with caution'
__prog_epilog__ = \
    'Note: This program ignores any non-image file in the target directory\n\n' \
    '*: Smaller hash sizes are better for detecting visually similar images, while larger hash sizes are better for\n' \
    '   identifying identical images; The smaller the hash size, the better the performance\n' \
    '\n' \
    '   Smallest accepted hash size is 8\n' \
    '\n' \
    'Algorithm: Average Hash (https://www.hackerfactor.com/blog/index.php?/archives/432-Looks-Like-It.html)'
