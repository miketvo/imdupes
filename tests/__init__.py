import os

URL_DATA_SRC = 'https://pokemondb.net/pokedex/national'
DIR_DATA = os.path.abspath('data/images/')
DIR_DATA_SCRAPED = os.path.join(DIR_DATA, 'scraped/')
DATA_DUPLICATE_PERCENTAGE = 0.2  # Percentage of images to be duplicated in test data
DATA_MAX_DUPLICATES = 3          # Maximum number of duplicated images in test data
DATA_RANDOM_SEED = 42            # Random seed for reproducibility of test data duplication process
