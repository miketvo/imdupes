# noinspection PyProtectedMember
from _version import __version__
import os
import shutil
from sys import platform
import sys
import zipfile
import tarfile
import hashlib
import PyInstaller.__main__


def build(specfile: str = None) -> None:
    if os.path.exists('build'):
        shutil.rmtree('build')

    if os.path.exists('dist'):
        shutil.rmtree('dist')

    PyInstaller.__main__.run([
        '--clean',
        f'{specfile}',
    ])


def create_zip_archive(os_name: str) -> None:
    with zipfile.ZipFile(f'dist/imdupes-v{__version__}-{os_name}.zip', 'w') as zipf:
        zipf.write('dist/imdupes.exe', arcname='imdupes.exe')


def create_tar_archive(os_name: str) -> None:
    with tarfile.open(f'dist/imdupes-v{__version__}-{os_name}.tar', 'w') as tar:
        tar.add('dist/imdupes', arcname='imdupes')


def create_checksum_file(os_name: str, file_extension: str) -> None:
    file_path = f'dist/imdupes-v{__version__}-{os_name}.{file_extension}'
    checksum = hashlib.sha256()
    with open(file_path, 'rb') as file:
        for chunk in iter(lambda: file.read(4096), b''):
            checksum.update(chunk)
    checksum_value = checksum.hexdigest()
    checksum_file_path = f'dist/imdupes-v{__version__}-{os_name}.{file_extension}.sha256'
    with open(checksum_file_path, 'w') as checksum_file:
        checksum_file.write(f'{checksum_value}  imdupes-v{__version__}-{os_name}.{file_extension}')


if __name__ == '__main__':
    print(f'Detected platform: "{platform}".', end='')
    if platform.startswith('win'):
        print('\n')
        build('windows-build.spec')
        create_zip_archive('windows')
        create_checksum_file('windows', 'zip')
    elif platform.startswith('linux'):
        print('\n')
        build('unix-build.spec')
        create_tar_archive('linux')
        create_checksum_file('linux', 'tar')
    elif platform.startswith('darwin'):
        print('\n')
        build('unix-build.spec')
        create_tar_archive('macos')
        create_checksum_file('macos', 'tar')
    else:
        print(f'Platform not supported!', file=sys.stderr)
        exit(-1)
