import os
import shutil
import random
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


from test import URL_DATA_SRC, DATA_DUPLICATE_PERCENTAGE, DATA_MAX_DUPLICATES, DATA_RANDOM_SEED
from test import DATA_DIR
from test.clean_test_data import clean


def crawl():
    print(
        f'Source: {URL_DATA_SRC}\n'
        f'Save directory: {DATA_DIR}\n'
    )

    # Access main Pokémon database for Generation 1 Pokémon
    response_master = requests.get(URL_DATA_SRC)
    soup_master = BeautifulSoup(response_master.content, 'html.parser')
    gen_1_title = soup_master.find('h2', {'id': 'gen-1'})
    gen_1_div = gen_1_title.find_next_sibling('div')

    # Crawl individual Pokémon
    if gen_1_div:
        urls_pokemon = [urljoin(URL_DATA_SRC, anchor_tag['href']) for anchor_tag in gen_1_div.select('.ent-name')]
        print(f'Found {len(urls_pokemon)} Pokémon in {URL_DATA_SRC} - Generation 1.')
        print(f'Downloading Pokémon Artworks...\n')
        for i, url_pokemon in enumerate(urls_pokemon, start=1):
            response_pokemon = requests.get(url_pokemon)
            soup_pokemon = BeautifulSoup(response_pokemon.content, 'html.parser')
            artwork_tags = soup_pokemon.select('[data-title*="official artwork"]')
            for artwork_tag in artwork_tags:
                url_download = artwork_tag['href']
                filename = url_download.split('/')[-1]

                with open(f'{DATA_DIR}/{filename}', 'wb') as f:
                    f.write(requests.get(url_download).content)
                    print(f'Saved {filename} [Pokémon {i}/{len(urls_pokemon)}]')
                    f.close()

    else:
        raise RuntimeError("No <div> element found after <h2 id='gen-1'>")

    print('\n[DONE]')


def generate():
    random.seed(DATA_RANDOM_SEED)
    print(
        f'Save directory: {DATA_DIR}\n'
        f'Duplicate percentage: {DATA_DUPLICATE_PERCENTAGE:.2f}\n'
        f'Max duplicates: {DATA_MAX_DUPLICATES}\n'
        f'Random seed: {DATA_RANDOM_SEED}\n'
    )

    filenames = os.listdir(DATA_DIR)
    print(f'Found {len(filenames)} images. Duplicating...\n')
    for i, filename in enumerate(filenames):
        print(f'Image {i + 1}/{len(filenames)}: {filename}', end='')
        num_duplicates = random.randint(1, DATA_MAX_DUPLICATES)
        if random.random() <= DATA_DUPLICATE_PERCENTAGE:
            for j in range(1, num_duplicates + 1):
                new_filename = f'DUPLICATE_{j}_{filename}'
                shutil.copy(f'{DATA_DIR}/{filename}', f'{DATA_DIR}/{new_filename}')
            print(f' was duplicated {num_duplicates} time(s).')
        else:
            print(f' was duplicated 0 time(s).')

    print('\n[DONE]')


if __name__ == '__main__':
    if len(os.listdir(DATA_DIR)) != 0:
        clean()
    crawl()
    generate()
