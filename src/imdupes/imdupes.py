from _version import __version__, __app_name__
from _version import __prog_usage__, __prog_desc__, __prog_epilog__
from _version import __scan_usage__, __scan_desc__, __scan_epilog__
from _version import __clean_usage__, __clean_desc__, __clean_epilog__

import os
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
        argument_parser.error(
            f'hash size of {arguments.hash_size} is too small, '
            f'see "{argument_parser.prog} {{scan,clean}} --help" for more info'
        )

    if arguments.mode == 'scan':
        if arguments.silent and arguments.output is None:
            argument_parser.error(
                f'scan mode -S/--silent flag requires -o/--output to be specified, '
                f'see "{argument_parser.prog} scan --help" for more info'
            )

        if not os.path.exists(arguments.directory):
            argument_parser.error(f'invalid path "{arguments.directory}"')
        if not os.path.isdir(arguments.directory):
            argument_parser.error(f'"{arguments.directory}" is not a directory')
        if len(os.listdir(arguments.directory)) == 0:
            cprint(f'"{arguments.directory}" is empty. Program terminated.', 'red')
            exit()

    if arguments.mode == 'clean':
        if not os.path.exists(arguments.input):
            argument_parser.error(f'invalid path "{arguments.input}"')
        if os.path.isdir(arguments.input) and len(os.listdir(arguments.input)) == 0:
            cprint(f'"{arguments.input}" is empty. Program terminated.', 'red')
            exit()

    return arguments


if __name__ == '__main__':
    try:
        # ============================================================================================================ #
        #                                             Arguments Processing                                             #
        # ============================================================================================================ #
        ap_top_level = argparse.ArgumentParser(
            prog=__app_name__,
            usage=__prog_usage__,
            description=__prog_desc__,
            epilog=__prog_epilog__,
            formatter_class=argparse.RawTextHelpFormatter
        )
        ap_top_level.add_argument(
            '-v', '--version', action='version', version=f'%(prog)s {__version__}',
            help='show version information and exit'
        )

        ap_common_args = argparse.ArgumentParser(add_help=False)
        ap_common_args.add_argument(
            '-s', '--hash-size',
            required=False, type=int, default=DEFAULT_HASH_SIZE,
            help=f'specify a preferred hash size (integer) (default: {DEFAULT_HASH_SIZE})*'
        )
        ap_common_args.add_argument(
            '-e', '--exclude', required=False, metavar='REGEX', help='exclude matched filenames based on REGEX pattern'
        )
        ap_common_args.add_argument(
            '-r', '--recursive', action='store_true',
            help='recursively search for images in subdirectories in addition to the specified parent directory'
        )
        ap_common_args.add_argument(
            '-V', '--verbose', type=int, choices=[0, 1, 2], default=0,
            help='explain what is being done (default: 0 - verbose mode off)'
        )

        subparsers = ap_top_level.add_subparsers(title='run modes', dest='mode', metavar='{scan,clean}', required=True)

        ap_scan = subparsers.add_parser(
            'scan', parents=[ap_common_args],
            usage=__scan_usage__,
            description=__scan_desc__,
            epilog=__scan_epilog__,
            formatter_class=argparse.RawTextHelpFormatter
        )
        ap_scan.add_argument('directory', help='target image directory')
        ap_scan.add_argument(
            '-H', '--show-hash', action='store_true',
            help='show hash value of each duplication in output'
        )
        ap_scan.add_argument(
            '-f', '--format', choices=[f.value for f in PathFormat], default=PathFormat.DIR_RELATIVE.value,
            help=f'console output file path format, (default: {PathFormat.DIR_RELATIVE.value})'
        )
        ap_scan.add_argument(
            '-S', '--silent', action='store_true', default=False,
            help=f'no console output, -o/--output must be specified'
        )
        ap_scan.add_argument(
            '-o', '--output', required=False, metavar='OUTPUT',
            help='save the output to the specified OUTPUT file (overwriting if file already exist)'
        )

        ap_clean = subparsers.add_parser(
            'clean', parents=[ap_common_args],
            usage=__clean_usage__,
            description=__clean_desc__,
            epilog=__clean_epilog__,
            formatter_class=argparse.RawTextHelpFormatter
        )
        ap_clean.add_argument(
            'input',
            help='a directory containing the target images to be processed and clean, or a valid text file\n'
                 'containing duplicated image paths (can be generated using scan mode using -o/--output flag)'
        )
        ap_clean.add_argument(
            '-i', '--interactive', action='store_true',
            help='prompt for every duplication and let the user choose which file to delete'
        )
        ap_clean.add_argument(
            '-f', '--format', choices=[f.value for f in PathFormat], default=PathFormat.DIR_RELATIVE.value,
            help=f'console output file path format, ignored if -V/--verbose and -i/--interactive are both not\n'
                 f'enabled (default: {PathFormat.DIR_RELATIVE.value})'
        )

        args = validate_args(ap_top_level)
        # ==== End Of Arguments Processing ===== #

        # ============================================================================================================ #
        #                                               Image Processing                                               #
        # ============================================================================================================ #
        if args.mode == 'scan':
            img_paths = index_images(
                args.directory,
                exclude=args.exclude,
                recursive=args.recursive,
                verbose=args.verbose
            )

            hashed_dups = detect_dup_images(
                img_paths,
                hash_size=args.hash_size,
                root_dir=args.directory,
                output_path_format=PathFormat(args.format),
                verbose=args.verbose
            )

            if not args.silent:
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
                    output_path_format=PathFormat.ABSOLUTE,
                    show_hash_cluster_header=args.show_hash,
                    file=file
                )
                file.close()
                if args.verbose > 0:
                    cprint(f'Output saved to "{args.output}"', 'blue', attrs=['bold'])

        elif args.mode == 'clean':
            img_paths = index_images(
                args.input,
                exclude=args.exclude,
                recursive=args.recursive,
                verbose=args.verbose
            )

            hashed_dups = detect_dup_images(
                img_paths, hash_size=args.hash_size,
                root_dir=args.input,
                output_path_format=PathFormat(args.format),
                verbose=args.verbose
            )

            clean(
                hashed_dups,
                root_dir=args.input,
                interactive=args.interactive,
                verbose=args.verbose,
                output_path_format=PathFormat(args.format)
            )

    except PermissionError as error:
        cprint(f'{error.__str__()}\nProgram terminated.', 'red')
        exit()
    except KeyboardInterrupt as error:
        exit()
