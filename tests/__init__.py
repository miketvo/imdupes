import os

URL_DATA_SRC = 'https://pokemondb.net/pokedex/national'
DATA_DIR = os.path.abspath('data/images/scraped/')
DATA_DUPLICATE_PERCENTAGE = 0.2  # Percentage of images to be duplicated in test data
DATA_MAX_DUPLICATES = 3          # Maximum number of duplicated images in test data
DATA_RANDOM_SEED = 42            # Random seed for reproducibility of test data duplication process
