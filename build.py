# noinspection PyProtectedMember
from imdupes._version import __version__
from sys import platform
import sys
import zipfile
import tarfile
import PyInstaller.__main__


def build(specfile: str = None) -> None:
    PyInstaller.__main__.run([
        '--clean',
        f'{specfile}',
    ])


def create_zip_archive(os_name: str) -> None:
    with zipfile.ZipFile(f'dist/imdupes-{__version__}-{os_name}.zip', 'w') as zipf:
        zipf.write('dist/imdupes.exe')


def create_tar_archive(os_name: str) -> None:
    with tarfile.open(f'dist/imdupes-{__version__}-{os_name}.tar', 'w') as tar:
        tar.add('dist/imdupes')


if __name__ == '__main__':
    print(f'Detected platform: "{platform}".', end='')
    if platform.startswith('win'):
        print('\n')
        build('windows-build.spec')
        create_zip_archive('windows')
    elif platform.startswith('linux'):
        print('\n')
        build('unix-build.spec')
        create_tar_archive('linux')
    elif platform.startswith('darwin'):
        print('\n')
        build('unix-build.spec')
        create_tar_archive('macos')
    else:
        print(f'Platform not supported!', file=sys.stderr)
        exit(-1)
