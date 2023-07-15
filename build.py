from sys import platform
import PyInstaller.__main__


def build(specfile: str = None):
    PyInstaller.__main__.run([
        '--clean',
        f'{specfile}',
    ])


if __name__ == '__main__':
    print(f'Detected platform: "{platform}".', end='')
    if platform.startswith('win'):
        print('\n')
        build('windows-build.spec')
    elif platform.startswith('linux') or platform.startswith('darwin'):
        print('\n')
        build('unix-build.spec')
    else:
        print(f'Platform not supported!')
