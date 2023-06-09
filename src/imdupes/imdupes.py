from _version import __version__, __app_name__
from _version import __prog_usage__, __prog_desc__, __prog_epilog__
from _version import __scan_usage__, __scan_desc__, __scan_epilog__
from _version import __clean_usage__, __clean_desc__, __clean_epilog__

import os
import sys
from sys import exit
import traceback
import argparse
from termcolor import cprint
from PIL import Image

import dupfile
from detect_dup_images import detect_dup_images
from utils.futils import index_images, clean
from utils.output import print_dups
from utils.globs import PathFormat
from utils.globs import DUPFILE_EXT
from utils.globs import DEFAULT_HASH_SIZE
from utils.globs import VERBOSE_LEVELS, PROGRESS_BAR_LEVELS


def validate_args(argument_parser: argparse.ArgumentParser) -> argparse.Namespace:
    arguments = argument_parser.parse_args()

    if arguments.hash_size < 8:
        argument_parser.error(
            f'hash size of {arguments.hash_size} is too small, '
            f'see "{argument_parser.prog} {{scan,clean}} --help" for more info'
        )
    if (arguments.verbose == 0) and any(argv.startswith(('-p', '--progress-bar')) for argv in sys.argv[1:]):
        argument_parser.error(
            f'-p/--progress-bar flag requires -V/--verbose to be specified, '
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

        if arguments.output is not None and arguments.output.split('.')[-1].lower() != DUPFILE_EXT:
            ext = arguments.output.split('.')[-1]
            argument_parser.error(
                f'output "{arguments.output}": invalid extension ".{ext}" (must be ".{DUPFILE_EXT}"), '
                f'see "{argument_parser.prog} scan --help" for more info'
            )

    if arguments.mode == 'clean':
        if not os.path.exists(arguments.input):
            argument_parser.error(f'invalid path "{arguments.input}"')
        if os.path.isfile(arguments.input) and arguments.recursive:
            argument_parser.error('cleaning from dupfile does not support -r/--recursive flag')
        if os.path.isfile(arguments.input) and any(argv.startswith(('-f', '--format')) for argv in sys.argv[1:]):
            argument_parser.error('cleaning from dupfile does not support -f/--format flag')
        if os.path.isfile(arguments.input) and any(argv.startswith(('-s', '--hash-size')) for argv in sys.argv[1:]):
            argument_parser.error('cleaning from dupfile does not support -s/--hash-size flag')
        if os.path.isfile(arguments.input) and any(argv.startswith(('-p', '--progress-bar')) for argv in sys.argv[1:]):
            argument_parser.error('cleaning from dupfile does not support -p/--progress-bar flag')
        if os.path.isfile(arguments.input) and arguments.input.split('.')[-1].lower() != DUPFILE_EXT:
            ext = arguments.input.split('.')[-1]
            cprint(
                f'"{arguments.input}": Invalid input file type ".{ext}". '
                f'Program terminated.', 'red'
            )
            exit()
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
            '-V', '--verbose', type=int, choices=VERBOSE_LEVELS, default=0,
            help='explain what is being done'
        )
        ap_common_args.add_argument(
            '-p', '--progress-bar', type=int, choices=PROGRESS_BAR_LEVELS, default=PROGRESS_BAR_LEVELS[-1],
            help=f'specify verbose mode (-V/--verbose) progress bar detail level, 0 disables the progress bar\n'
                 f'entirely (default: {PROGRESS_BAR_LEVELS[-1]})'
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
            '-S', '--silent', action='store_true',
            help=f'no console output, -o/--output must be specified'
        )
        ap_scan.add_argument(
            '-o', '--output', required=False, metavar='DUPFILE',
            help=f'save the output to the specified DUPFILE (JSON formatted .{DUPFILE_EXT}) file (overwriting if file\n'
                 'already exist)'
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
            help='a directory containing the target images to be processed and clean; or a valid JSON formatted\n'
                 f'.{DUPFILE_EXT} file containing duplicated image paths (can be generated using scan mode with\n'
                 '-o/--output\n flag), in which case only the following flags are available:\n'
                 '  -h/--help\n'
                 '  -e/--exclude\n'
                 '  -V/--verbose\n'
                 '  -i/--interactive\n'
                 'see options below for more information'
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
                verbose=args.verbose,
                progress_bar=args.progress_bar
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
                dupfile.save(
                    [dup_imgs for dup_imgs in hashed_dups.values()],
                    file=args.output,
                    verbose=args.verbose
                )

        elif args.mode == 'clean':
            if os.path.isfile(args.input):
                dups = dupfile.load(
                    args.input,
                    exclude=args.exclude,
                    verbose=args.verbose
                )

                clean(
                    dups,
                    interactive=args.interactive,
                    verbose=args.verbose,
                    output_path_format=PathFormat.ABSOLUTE
                )

            else:
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
                    verbose=args.verbose,
                    progress_bar=args.progress_bar
                )

                clean(
                    [dup_imgs for dup_imgs in hashed_dups.values()],
                    root_dir=args.input,
                    interactive=args.interactive,
                    verbose=args.verbose,
                    output_path_format=PathFormat(args.format)
                )

    except KeyboardInterrupt:
        exit()
    except (
            ValueError, TypeError,
            Image.DecompressionBombError,
            OSError, EOFError, PermissionError,
            MemoryError
    ) as error:
        cprint(f'\nFatal error: {error.__str__()}\nProgram terminated.', 'red')
        exit()
    except (Exception,) as exception:  # Do not remove this comma, lest thou seek the wrath of PEP 8 gods
        cprint(f'\nUnknown fatal error:', 'red')
        traceback.print_exc()
        cprint(f'Program terminated.', 'red')
        exit()
