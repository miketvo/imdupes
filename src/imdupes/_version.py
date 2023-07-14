__version__ = '0.2.4'
__app_name__ = 'imdupes'

__prog_usage__ = f'{__app_name__} {{info,scan,clean}} ...'
__prog_desc__ = \
    'Quickly detects and removes identical images. Has 3 modes:\n' \
    "\t- 'info' collects and displays statistics and information of images in a directory\n" \
    "\t- 'scan' scans and console prints detected identical image paths/filenames\n" \
    "\t- 'clean' scans and removes detected identical images (keeping only the first copy by default)\n" \
    f'See "{__app_name__} {{info,scan,clean}} --help" for more information'
__prog_epilog__ = \
    'Note: This program ignores any non-image file in the target directory\n' \
    'Algorithm: Average Hash (https://www.hackerfactor.com/blog/index.php?/archives/432-Looks-Like-It.html)'

__info_usage__ = f'{__app_name__} info [options] directory'
__info_desc__ = \
    'collect and display statistics and information of images in a directory'
__info_epilog__ = \
    'Note: This program ignores any non-image file in the target directory'

__scan_usage__ = f'{__app_name__} scan [options] directory [-o OUTPUT]'
__scan_desc__ = \
    'scan and console print detected identical image paths/filenames'
__scan_epilog__ = \
    'Note: This program ignores any non-image file in the target directory\n' \
    '*: Smaller hash sizes are better for detecting visually similar images, while larger hash sizes are better for\n' \
    '   identifying identical images; The smaller the hash size, the better the performance; Smallest accepted hash ' \
    'size\n   is 8' \

__clean_usage__ = f'{__app_name__} clean [options] input'
__clean_desc__ = \
    'scan and remove detected identical images (keeping only the first copy by default); deleted files are not\n' \
    'recoverable, proceed with caution'
__clean_epilog__ = __scan_epilog__
