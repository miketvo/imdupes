import argparse


if __name__ == '__main__':
    ap = argparse.ArgumentParser(
        prog='imdupes',
        description=
        "Quickly detects and removes identical images. Has two modes:\n"
        "\t- 'detect' console prints the detected identical images path/filename\n"
        "\t- 'clean' removes the detected identical images",
        epilog='Note: This program ignores any non-image file in the target directory',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    ap.add_argument('mode', choices=['detect', 'clean'], help="run mode")
    ap.add_argument('directory', help='target image directory')
    ap.add_argument(
        '-e', '--exclude', required=False, metavar='REGEX', help='exclude matched file names based on REGEX pattern'
    )
    ap.add_argument(
        '-r', '--recursive', action='store_true',
        help='recursively search for images in subdirectories in addition to the specified parent directory'
    )
    ap.add_argument(
        '-v', '--verbose', action='store_true', help='verbose mode'
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
        '-y', '--no-confirm', action='store_true', help='no asking for user confirmation before file deletion'
    )

    args = ap.parse_args()
    print(args)
