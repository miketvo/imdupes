import PyInstaller.__main__


def build():
    PyInstaller.__main__.run([
        'src/imdupes/imdupes.py',
        '--onefile',
        '--icon', 'icon.png',
        '--console',
        '--clean'
    ])

    PyInstaller.__main__.run([
        'src/imdupes/wimdupes.pyw',
        '--onefile',
        '--icon', 'icon.png',
        '--windowed',
        '--clean'
    ])


if __name__ == '__main__':
    build()
