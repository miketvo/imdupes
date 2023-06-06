from _version import __version__, __app_name__
from _version import __prog_usage__, __prog_desc__, __prog_epilog__

import os
import sys
from sys import exit
import argparse
from termcolor import cprint

from detect_dup_images import detect_dup_images
from utils.futils import index_images, clean
from utils.output import print_dups
from utils.globs import PathFormat
from utils.globs import DEFAULT_HASH_SIZE


def validate_args(argument_parser: argparse.ArgumentParser) -> argparse.Namespace:
    arguments = argument_parser.parse_args()

    if arguments.hash_size < 8:
        ap.error(f'Hash size {arguments.hash_size} too small, see {ap.prog} --help for more info')

    if arguments.mode == 'scan':
        if arguments.interactive:
            ap.error(f'scan mode does not support -i/--interactive flag, see {ap.prog} --help for more info')

    if arguments.mode == 'clean':
        if arguments.output:
            ap.error(f'clean mode does not support -o/--output flag, see {ap.prog} --help for more info')
        if arguments.show_hash:
            ap.error(f'clean mode does not support -H/--show-hash flag, see {ap.prog} --help for more info')
        if ('-f' in sys.argv[1:] or '--format' in sys.argv[1:]) and (not arguments.verbose):
            ap.error(
                f'clean mode -f/--format requires -V/--verbose flags to be used in conjunction, '
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
            formatter_class=argparse.RawTextHelpFormatter
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
            help='console output file path format; '
                 'always applied to scan mode, applied to clean mode only when\nverbose is enabled '
                 f'(default: {PathFormat.DIR_RELATIVE.value})'
        )
        ap.add_argument(
            '-H', '--show-hash', action='store_true',
            help='show hash value of each duplication in output'
        )
        ap.add_argument(
            '-v', '--version', action='version', version=f'%(prog)s {__version__}',
            help='show version information and exit'
        )

        scan_options = ap.add_argument_group('scan mode options')
        scan_options.add_argument(
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
            verbose=args.verbose
        )

        if args.mode == 'scan':
            hashed_dups = detect_dup_images(
                img_paths,
                hash_size=args.hash_size,
                root_dir=args.directory,
                output_path_format=PathFormat(args.format),
                verbose=args.verbose
            )

            print()
            print_dups(
                hashed_dups,
                root_dir=args.directory,
                output_path_format=PathFormat(args.format),
                colored_cluster_header=True,
                show_hash_cluster_header=args.show_hash
            )

            if args.output is not None:
                file = open(args.output, 'w')
                print_dups(
                    hashed_dups,
                    root_dir=args.directory,
                    output_path_format=PathFormat(args.format),
                    show_hash_cluster_header=args.show_hash,
                    file=file
                )
                file.close()
                if args.verbose > 0:
                    cprint(f'Output saved to "{args.output}"', 'blue', attrs=['bold'])

        elif args.mode == 'clean':
            hashed_dups = detect_dup_images(
                img_paths, hash_size=args.hash_size,
                root_dir=args.directory,
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
