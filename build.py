from sys import platform
import PyInstaller.__main__


def build(specfile: str = None):
    PyInstaller.__main__.run([
        'src/imdupes/imdupes.py',
        '--clean',
        f'{specfile}'
    ])


if __name__ == '__main__':
    if platform.startswith('win'):
        build('windows-build.spec')
    elif platform.startswith('linux'):
        build('linux-build.spec')
    else:
        print(f'Platform "{platform}" not supported!')
