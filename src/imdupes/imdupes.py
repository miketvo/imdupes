from _version import __version__, __app_name__
import argparse

from detect import detect
from utils import PathFormat


def validate_args(argument_parser: argparse.ArgumentParser) -> argparse.Namespace:
    arguments = argument_parser.parse_args()
    if arguments.mode == 'detect':
        if arguments.interactive:
            ap.error(f'detect mode does not support -i/--interactive flag, see {ap.prog} --help for more info')
    if arguments.mode == 'clean':
        if arguments.output:
            ap.error(f'clean mode does not support -o/--output flag, see {ap.prog} --help for more info')

    return arguments


if __name__ == '__main__':
    ap = argparse.ArgumentParser(
        prog=__app_name__,
        usage='imdupes {detect,clean} [OPTIONS] DIRECTORY',
        description="Quickly detects and removes identical images. Has two modes:\n"
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
        '-p', '--progress-bar', action='store_true',
        help='display a progress bar'
    )
    ap.add_argument(
        '-V', '--verbose', action='store_true', help='explain what is being done'
    )
    ap.add_argument(
        '-v', '--version', action='version', version=f'%(prog)s {__version__}', help='show version information and exit'
    )

    detect_options = ap.add_argument_group('detect mode options')
    detect_options.add_argument(
        '-f', '--format', choices=[f.value for f in PathFormat], default=PathFormat.ABSOLUTE,
        help='console output file path format (default: absolute)'
    )
    detect_options.add_argument(
        '-o', '--output', required=False, metavar='OUTPUT', help='save the console output to the specified OUTPUT file'
    )

    clean_options = ap.add_argument_group('clean mode options')
    clean_options.add_argument(
        '-i', '--interactive', action='store_true', help='prompt before every file deletion'
    )

    args = validate_args(ap)

    duplicate_paths = detect(
        args.directory,
        exclude=args.exclude,
        recursive=args.recursive,
        output_format=PathFormat(args.format),
        progress_bar=args.progress_bar,
        verbose=args.verbose
    )

    print(duplicate_paths)
