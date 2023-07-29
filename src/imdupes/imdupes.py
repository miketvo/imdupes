from _version import __version__, __app_name__
from _version import __prog_usage__, __prog_desc__, __prog_epilog__
from _version import __info_usage__, __info_desc__, __info_epilog__
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
from utils.imutils import report_info, calc_hash_size
from utils.imutils import ImageFileWrapper
from utils.output import print_dups
from utils.globs import PathFormat
from utils.globs import HashingMethod
from utils.globs import AutoHashSize
from utils.globs import DUPFILE_EXT
from utils.globs import VERBOSE_LEVELS, PROGRESS_BAR_LEVELS


def validate_args(argument_parser: argparse.ArgumentParser) -> argparse.Namespace:
    arguments = argument_parser.parse_args()

    if arguments.mode in ['scan', 'clean']:
        if arguments.hash_size is not None and arguments.hash_size < 8:
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
            if os.path.isfile(arguments.input) \
                    and any(argv.startswith(('-p', '--progress-bar')) for argv in sys.argv[1:]):
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


def main(arguments: argparse.Namespace) -> None:
    def find_dups() -> dict[str, list[ImageFileWrapper]]:
        directory = arguments.input if arguments.mode == 'clean' else arguments.directory

        image_paths = index_images(
            directory,
            exclude=arguments.exclude,
            recursive=arguments.recursive,
            verbose=arguments.verbose
        )

        if arguments.hash_size is None:
            hash_size, image_paths = calc_hash_size(
                image_paths,
                auto_hash_size=AutoHashSize(arguments.auto_hash_size),
                verbose=arguments.verbose,
                progress_bar=arguments.progress_bar,
                output_path_format=PathFormat(arguments.format),
                root_dir=directory
            )
        else:
            hash_size = arguments.hash_size

        return detect_dup_images(
            image_paths,
            method=HashingMethod(arguments.hashing_method),
            hash_size=hash_size,
            root_dir=directory,
            output_path_format=PathFormat(arguments.format),
            verbose=arguments.verbose,
            progress_bar=arguments.progress_bar
        )

    if arguments.mode == 'info':
        image_paths = index_images(
            arguments.directory,
            exclude=arguments.exclude,
            recursive=arguments.recursive,
            verbose=arguments.verbose
        )

        report_info(
            image_paths,
            verbose=arguments.verbose,
            progress_bar=arguments.progress_bar,
            output_path_format=PathFormat(arguments.format),
            root_dir=arguments.directory
        )

    elif arguments.mode == 'scan':
        hashed_dups = find_dups()

        if not arguments.silent:
            print()
            print_dups(
                hashed_dups,
                root_dir=arguments.directory,
                output_path_format=PathFormat(arguments.format),
                colored_cluster_header=True,
                show_hash_cluster_header=arguments.show_hash
            )

        if arguments.output is not None:
            dupfile.save(
                [dup_imgs for dup_imgs in hashed_dups.values()],
                file=arguments.output,
                verbose=arguments.verbose
            )

    elif arguments.mode == 'clean':
        if os.path.isfile(arguments.input):
            dups = dupfile.load(
                arguments.input,
                exclude=arguments.exclude,
                verbose=arguments.verbose
            )

            clean(
                dups,
                interactive=arguments.interactive,
                verbose=arguments.verbose,
                output_path_format=PathFormat.ABSOLUTE
            )

        else:
            hashed_dups = find_dups()

            clean(
                [dup_imgs for dup_imgs in hashed_dups.values()],
                root_dir=arguments.input,
                interactive=arguments.interactive,
                verbose=arguments.verbose,
                output_path_format=PathFormat(arguments.format)
            )


if __name__ == '__main__':
    try:
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

        ap_scan_clean_specific_args = argparse.ArgumentParser(add_help=False)
        ap_scan_clean_specific_args.add_argument(
            '-m', '--hashing-method', choices=[m.value for m in HashingMethod], default=HashingMethod.HIST.value,
            help=f'specify a hashing method (default: {HashingMethod.HIST.value})'
        )
        ap_scan_clean_specific_hash_size_args = ap_scan_clean_specific_args.add_mutually_exclusive_group()
        ap_scan_clean_specific_hash_size_args.add_argument(
            '-a', '--auto-hash-size', choices=[a.value for a in AutoHashSize], default=AutoHashSize.MAX_DIMS_MEAN.value,
            help=f'automatic hash size calculation (default: {AutoHashSize.MAX_DIMS_MEAN.value})'
        )
        ap_scan_clean_specific_hash_size_args.add_argument(
            '-s', '--hash-size', required=False, type=int, default=None,
            help=f'specify a preferred hash size (integer)*'
        )

        subparsers = ap_top_level.add_subparsers(
            title='run modes', metavar='{info,scan,clean}',
            dest='mode', required=True
        )

        ap_info = subparsers.add_parser(
            'info', parents=[ap_common_args],
            usage=__info_usage__,
            description=__info_desc__,
            epilog=__info_epilog__,
            formatter_class=argparse.RawTextHelpFormatter
        )
        ap_info.add_argument('directory', help='target image directory')
        ap_info.add_argument(
            '-f', '--format', choices=[f.value for f in PathFormat], default=PathFormat.DIR_RELATIVE.value,
            help=f'console output file path format, (default: {PathFormat.DIR_RELATIVE.value})'
        )

        ap_scan = subparsers.add_parser(
            'scan', parents=[ap_scan_clean_specific_args, ap_common_args],
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
            'clean', parents=[ap_scan_clean_specific_args, ap_common_args],
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
        main(arguments=args)

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
