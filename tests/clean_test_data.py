import os

from tests import DATA_DIR


def clean():
    print(f'Cleaning test data...', end='')
    for file in os.listdir(DATA_DIR):
        os.remove(f'{DATA_DIR}/{file}')
    print(' [DONE]')


if __name__ == '__main__':
    clean()
