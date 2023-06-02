import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


URL_MASTER = 'https://pokemondb.net/pokedex/national'
SAVE_DIR = os.path.abspath('../data/')


if __name__ == '__main__':
    print(
        f'Source: {URL_MASTER}\n'
        f'Save directory: {SAVE_DIR}\n'
    )

    # Access main Pokémon database for Generation 1 Pokémon
    response_master = requests.get(URL_MASTER)
    soup_master = BeautifulSoup(response_master.content, 'html.parser')
    gen_1_title = soup_master.find('h2', {'id': 'gen-1'})
    gen_1_div = gen_1_title.find_next_sibling('div')

    # Crawl individual Pokémon
    if gen_1_div:
        urls_pokemon = [urljoin(URL_MASTER, anchor_tag['href']) for anchor_tag in gen_1_div.select('.ent-name')]
        print(f'Found {len(urls_pokemon)} Pokémon in {URL_MASTER} - Generation 1.')
        print(f'Downloading Pokémon Artworks...\n')
        for i, url_pokemon in enumerate(urls_pokemon, start=1):
            response_pokemon = requests.get(url_pokemon)
            soup_pokemon = BeautifulSoup(response_pokemon.content, 'html.parser')
            artwork_tags = soup_pokemon.select('[data-title*="official artwork"]')
            for artwork_tag in artwork_tags:
                url_download = artwork_tag['href']
                filename = url_download.split('/')[-1]

                with open(f'{SAVE_DIR}/{filename}', 'wb') as f:
                    f.write(requests.get(url_download).content)
                    print(f'Saved {filename} [Pokémon {i}/{len(urls_pokemon)}]')
                    f.close()

    else:
        raise RuntimeError("No <div> element found after <h2 id='gen-1'>")

    print('\n[DONE]')
