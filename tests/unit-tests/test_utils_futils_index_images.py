import unittest
import sys
import os
from os.path import dirname


sys.path.append(os.path.join(dirname(__file__) + '/../..', 'src/imdupes'))
sys.path.append(os.path.join(dirname(__file__) + '/../..', 'tests'))
from utils.futils import index_images
from tests import DIR_DATA_SCRAPED


class ExcludeFilename(unittest.TestCase):
    def test_prefix_exclude(self):
        # Arrange
        def get_test_image_paths() -> list[str]:
            paths = set()

            for filename in os.listdir(DIR_DATA_SCRAPED):
                filename_tokens = filename.split('_')
                if filename_tokens[0] != 'DUPLICATE':
                    paths.add(os.path.abspath(DIR_DATA_SCRAPED + filename))

            return list(paths)
        test_image_paths = get_test_image_paths()

        # Act
        image_paths = index_images(
            DIR_DATA_SCRAPED,
            exclude='^DUPLICATE',
            recursive=False,
            verbose=0
        )

        # Assert
        self.assertCountEqual(test_image_paths, image_paths)

    def test_postfix_exclude(self):
        # Arrange & Act
        image_paths = index_images(
            DIR_DATA_SCRAPED,
            exclude='.jpg$',
            recursive=False,
            verbose=0
        )

        # Assert
        self.assertEquals(0, len(image_paths))


if __name__ == '__main__':
    unittest.main()
