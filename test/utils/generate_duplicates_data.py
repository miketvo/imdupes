import os
import random
import shutil


SAVE_DIR = os.path.abspath('../data/')
DUPLICATE_PERCENTAGE = 0.2  # Percentage of images to be duplicated
MAX_DUPLICATES = 3          # Maximum number of duplicated images
RANDOM_SEED = 42            # Random seed for reproducibility


if __name__ == '__main__':
    random.seed(RANDOM_SEED)
    print(
        f'Save directory: {SAVE_DIR}\n'
        f'Duplicate percentage: {DUPLICATE_PERCENTAGE:.2f}\n'
        f'Max duplicates: {MAX_DUPLICATES}\n'
        f'Random seed: {RANDOM_SEED}\n'
    )

    filenames = os.listdir(SAVE_DIR)
    print(f'Found {len(filenames)} images. Duplicating...\n')
    for i, filename in enumerate(filenames):
        print(f'Image {i + 1}/{len(filenames)}: {filename}', end='')
        num_duplicates = random.randint(1, MAX_DUPLICATES)
        if random.random() <= DUPLICATE_PERCENTAGE:
            for j in range(1, num_duplicates + 1):
                new_filename = f'DUPLICATE_{j}_{filename}'
                shutil.copy(f'{SAVE_DIR}/{filename}', f'{SAVE_DIR}/{new_filename}')
            print(f' was duplicated {num_duplicates} time(s).')
        else:
            print(f' was duplicated 0 time(s).')

    print('\n[DONE]')
