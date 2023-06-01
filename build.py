import PyInstaller.__main__


def build():
    PyInstaller.__main__.run([
        'src/imdupes/imdupes.py',
        '--console',
        '--clean'
    ])


if __name__ == '__main__':
    build()
