import unittest
import sys
import os
from os.path import dirname


sys.path.append(os.path.join(dirname(__file__) + '/../..', 'src/imdupes'))
sys.path.append(os.path.join(dirname(__file__) + '/../..', 'tests'))
from utils.futils import index_images
from utils.globs import SUPPORTED_FILE_EXTS
from tests import DIR_DATA_SCRAPED
from tests import DIR_DATA


class ExcludeFilename(unittest.TestCase):
    def test_prefix_exclude(self):
        # Arrange
        def get_test_image_paths() -> list[str]:
            paths = set()

            for filename in os.listdir(DIR_DATA_SCRAPED):
                if not filename.startswith('DUPLICATE'):
                    paths.add(os.path.abspath(os.path.join(DIR_DATA_SCRAPED, filename)))

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
        self.maxDiff = None
        self.assertCountEqual(test_image_paths, image_paths)

    def test_postfix_exclude(self):
        # Arrange
        def get_test_image_paths() -> list[str]:
            paths = set()

            for filename in os.listdir(DIR_DATA):
                if (not filename.endswith('jpg')) and (filename.split('.')[-1] in SUPPORTED_FILE_EXTS):
                    paths.add(os.path.abspath(os.path.join(DIR_DATA, filename)))

            return list(paths)
        test_image_paths = get_test_image_paths()

        # Act
        image_paths = index_images(
            DIR_DATA,
            exclude='.jpg$',
            recursive=True,
            verbose=0
        )

        # Assert
        self.maxDiff = None
        self.assertCountEqual(test_image_paths, image_paths)

    def test_pattern_exclude(self):
        # Arrange
        def get_test_image_paths() -> list[str]:
            paths = set()

            for filename in os.listdir(DIR_DATA_SCRAPED):
                if filename.find('abr') == -1 and filename.find('arb') == -1:
                    paths.add(os.path.abspath(os.path.join(DIR_DATA_SCRAPED, filename)))

            return list(paths)
        test_image_paths = get_test_image_paths()

        # Act
        image_paths = index_images(
            DIR_DATA_SCRAPED,
            exclude='abr|arb',
            recursive=False,
            verbose=0
        )

        # Assert
        self.maxDiff = None
        self.assertCountEqual(test_image_paths, image_paths)


if __name__ == '__main__':
    unittest.main()
