import unittest
import sys
import os
from os.path import dirname


sys.path.append(os.path.join(dirname(__file__) + '/../..', 'src/imdupes'))
sys.path.append(os.path.join(dirname(__file__) + '/../..', 'tests'))
from utils.futils import index_images
from tests import DIR_DATA_SCRAPED


def get_test_image_paths() -> list[str]:
    paths = set()

    for filename in os.listdir(DIR_DATA_SCRAPED):
        filename_tokens = filename.split('_')
        if filename_tokens[0] != 'DUPLICATE':
            paths.add(os.path.abspath(DIR_DATA_SCRAPED + filename))

    return list(paths)


class ExcludeFile(unittest.TestCase):
    def test_prefix_exclude(self):
        # Arrange
        test_image_paths = get_test_image_paths()

        # Act
        image_paths = index_images(
            DIR_DATA_SCRAPED,
            exclude='^DUPLICATE',
            recursive=False,
            verbose=2
        )

        # Assert
        self.maxDiff = None
        self.assertCountEqual(test_image_paths, image_paths)


if __name__ == '__main__':
    unittest.main()
