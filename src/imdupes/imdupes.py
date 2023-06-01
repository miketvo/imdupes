from _version import __version__
import argparse


if __name__ == '__main__':
    ap = argparse.ArgumentParser(
        prog='imdupes',
        description=
        "Quickly detects and removes identical images. Has two modes:\n"
        "\t- 'detect' console prints the detected identical image paths/filenames\n"
        "\t- 'clean' removes the detected identical images",
        epilog='Note: This program ignores any non-image file in the target directory',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    ap.add_argument('mode', choices=['detect', 'clean'], help="run mode")
    ap.add_argument('directory', help='target image directory')
    ap.add_argument(
        '-e', '--exclude', required=False, metavar='REGEX', help='exclude matched filenames based on REGEX pattern'
    )
    ap.add_argument(
        '-r', '--recursive', action='store_true',
        help='recursively search for images in subdirectories in addition to the specified parent directory'
    )
    ap.add_argument(
        '-V', '--verbose', action='store_true', help='explain what is being done'
    )
    ap.add_argument(
        '-v', '--version', action='version', version=f'%(prog)s {__version__}', help='show version information and exit'
    )

    detect_options = ap.add_argument_group('detect mode options')
    detect_options.add_argument(
        '-f', '--format', choices=['absolute', 'relative', 'filename'], default='absolute',
        help='console output file path format (default: absolute)'
    )
    detect_options.add_argument(
        '-o', '--output', required=False, metavar='OUTPUT', help='save the console output to the specified OUTPUT file'
    )

    clean_options = ap.add_argument_group('clean mode options')
    clean_options.add_argument(
        '-i', '--interactive', action='store_true', help='prompt before every file deletion'
    )

    args = ap.parse_args()
    print(args)
