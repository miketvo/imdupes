import os

from tests import DIR_DATA_SCRAPED


def clean():
    print(f'Cleaning test data...', end='')
    for file in os.listdir(DIR_DATA_SCRAPED):
        os.remove(f'{DIR_DATA_SCRAPED}/{file}')
    print(' [DONE]')


if __name__ == '__main__':
    clean()
