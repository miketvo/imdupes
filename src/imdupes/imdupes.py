from _version import __version__, __app_name__
from _version import __prog_usage__, __prog_desc__, __prog_epilog__

import os
import sys
from sys import exit
import argparse
from termcolor import cprint

from detect_dup_imgs import detect_dup_imgs
from utils.futils import index_images, clean
from utils.globs import PathFormat, format_path
from utils.globs import DEFAULT_HASH_SIZE


def validate_args(argument_parser: argparse.ArgumentParser) -> argparse.Namespace:
    arguments = argument_parser.parse_args()

    if arguments.hash_size < 8:
        ap.error(f'Hash size {arguments.hash_size} too small, see {ap.prog} --help for more info')

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
    try:
        # ============================================================================================================ #
        #                                             Arguments Processing                                             #
        # ============================================================================================================ #
        ap = argparse.ArgumentParser(
            prog=__app_name__,
            usage=__prog_usage__,
            description=__prog_desc__,
            epilog=__prog_epilog__,
            formatter_class=argparse.RawDescriptionHelpFormatter
        )

        ap.add_argument('mode', choices=['scan', 'clean'], help="run mode")
        ap.add_argument('directory', help='target image directory')
        ap.add_argument(
            '-s', '--hash-size',
            required=False, type=int, default=DEFAULT_HASH_SIZE,
            help=f'specify a preferred hash size (integer) (default: {DEFAULT_HASH_SIZE})*'
        )
        ap.add_argument(
            '-e', '--exclude', required=False, metavar='REGEX', help='exclude matched filenames based on REGEX pattern'
        )
        ap.add_argument(
            '-r', '--recursive', action='store_true',
            help='recursively search for images in subdirectories in addition to the specified parent directory'
        )
        ap.add_argument(
            '-V', '--verbose', type=int, choices=[0, 1, 2], default=0,
            help='explain what is being done (default: 0 - verbose mode off)'
        )
        ap.add_argument(
            '-f', '--format', choices=[f.value for f in PathFormat], default=PathFormat.DIR_RELATIVE.value,
            help='console output file path format, '
                 'always applied to detect mode and clean mode only when verbose is enabled '
                 f'(default: {PathFormat.DIR_RELATIVE.value})'
        )
        ap.add_argument(
            '-v', '--version', action='version', version=f'%(prog)s {__version__}',
            help='show version information and exit'
        )

        detect_options = ap.add_argument_group('detect mode options')
        detect_options.add_argument(
            '-o', '--output', required=False, metavar='OUTPUT',
            help='save the console output to the specified OUTPUT file (overwriting if file already exist)'
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

        # ============================================================================================================ #
        #                                               Image Processing                                               #
        # ============================================================================================================ #
        img_paths = index_images(
            args.directory,
            exclude=args.exclude,
            recursive=args.recursive,
            verbose=args.verbose,
        )

        if args.mode == 'scan':
            hashed_dups = detect_dup_imgs(
                img_paths,
                hash_size=args.hash_size,
                root_dir=args.directory,
                output_path_format=PathFormat(args.format),
                verbose=args.verbose
            )

            if args.output is not None:
                f = open(args.output, 'w')
                for dup_imgs in hashed_dups.values():
                    for dup_img in dup_imgs:
                        f.write(f'{format_path(dup_img.path, PathFormat(args.format), args.directory)}\n')
                    f.write('\n')
                if args.verbose:
                    cprint(f'Output saved to "{args.output}"', 'blue', attrs=['bold'])

        elif args.mode == 'clean':
            hashed_dups = detect_dup_imgs(
                img_paths, hash_size=args.hash_size,
                root_dir=args.directory,
                console_output=False,
                output_path_format=PathFormat(args.format),
                verbose=args.verbose
            )

            clean(
                hashed_dups,
                root_dir=args.directory,
                interactive=args.interactive,
                verbose=args.verbose,
                output_path_format=PathFormat(args.format)
            )

    except PermissionError as error:
        cprint(f'{error.__str__()}\nProgram terminated.', 'red')
        exit()
    except KeyboardInterrupt as error:
        exit()
