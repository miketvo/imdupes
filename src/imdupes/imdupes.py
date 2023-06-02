from _version import __version__, __app_name__

import os
import sys
import argparse
from termcolor import cprint

from detect import detect
from utils.futils import index_images, clean
from utils.globs import PathFormat


def validate_args(argument_parser: argparse.ArgumentParser) -> argparse.Namespace:
    arguments = argument_parser.parse_args()
    if arguments.mode == 'detect':
        if arguments.interactive:
            ap.error(f'detect mode does not support -i/--interactive flag, see {ap.prog} --help for more info')
    if arguments.mode == 'clean':
        if arguments.output:
            ap.error(f'clean mode does not support -o/--output flag, see {ap.prog} --help for more info')
        if ('-f' in sys.argv[1:] or '--format' in sys.argv[1:]) and (not arguments.verbose):
            ap.error(
                f'clean mode requires -f/--format and -V/--verbose flags to be used together, '
                f'see {ap.prog} --help for more info'
            )

    return arguments


if __name__ == '__main__':
    # ================================================================================================================ #
    #                                               Arguments Processing                                               #
    # ================================================================================================================ #
    ap = argparse.ArgumentParser(
        prog=__app_name__,
        usage='imdupes {detect,clean} [OPTIONS] DIRECTORY',
        description="Quickly detects and removes identical images. Has two modes:\n"
                    "\t- 'detect' console prints the detected identical image paths/filenames\n"
                    "\t- 'clean' removes the detected identical images, keeping only the first copy",
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
        '-f', '--format', choices=[f.value for f in PathFormat], default=PathFormat.DIR_RELATIVE.value,
        help='console output file path format, '
             'always applied to detect mode and clean mode only when verbose is enabled '
             f'(default: {PathFormat.DIR_RELATIVE.value})'
    )
    ap.add_argument(
        '-v', '--version', action='version', version=f'%(prog)s {__version__}', help='show version information and exit'
    )

    detect_options = ap.add_argument_group('detect mode options')
    detect_options.add_argument(
        '-o', '--output', required=False, metavar='OUTPUT', help='save the console output to the specified OUTPUT file'
    )

    clean_options = ap.add_argument_group('clean mode options')
    clean_options.add_argument(
        '-i', '--interactive', action='store_true',
        help='prompt before every file deletion and let the user choose which file to delete'
    )

    args = validate_args(ap)
    if not os.path.exists(args.directory):
        cprint(f'Invalid path provided: "{args.directory}". Program terminated.', 'red')
        exit()
    if not os.path.isdir(args.directory):
        cprint(f'"{args.directory}" is not a directory. Program terminated.', 'red')
        exit()
    if len(os.listdir(args.directory)) == 0:
        cprint(f'"{args.directory}" is empty. Program terminated.', 'red')
        exit()
    # ==== End Of Arguments Processing ===== #

    # ================================================================================================================ #
    #                                                 Image Processing                                                 #
    # ================================================================================================================ #
    img_paths = index_images(
        args.directory,
        exclude=args.exclude,
        recursive=args.recursive,
        verbose=args.verbose,
        output_path_format=PathFormat(args.format)
    )

    if args.mode == 'detect':
        detect(
            img_paths,
            output_path_format=PathFormat(args.format),
            progress_bar=args.progress_bar,
            verbose=args.verbose,
        )

    elif args.mode == 'clean':
        dup_img_paths = detect(
            img_paths,
            console_output=False,
            output_path_format=PathFormat(args.format),
            progress_bar=args.progress_bar,
            verbose=args.verbose
        )

        clean(
            img_paths,
            interactive=args.interactive,
            progress_bar=args.progress_bar,
            verbose=args.verbose,
            output_path_format=PathFormat(args.format)
        )
