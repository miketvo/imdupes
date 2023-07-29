import unittest
import sys
import os
from os.path import dirname


sys.path.append(os.path.join(dirname(__file__) + '/../..', 'src/imdupes'))
sys.path.append(os.path.join(dirname(__file__) + '/../..', 'tests'))
from detect_dup_images import detect_dup_images
from utils.globs import HashingMethod
from tests import DIR_DATA_SCRAPED


class DetectDupImages(unittest.TestCase):
    def test(self):
        # Arrange
        def get_test_dups() -> list[str]:
            dups = set()

            for filename in os.listdir(DIR_DATA_SCRAPED):
                if filename.startswith('DUPLICATE_'):
                    dups.add(filename)
                    dups.add(filename.split('_')[-1])

            return list(dups)
        test_dups = get_test_dups()

        # Act
        detect_dups_dict = detect_dup_images(
            [os.path.join(DIR_DATA_SCRAPED, img) for img in os.listdir(DIR_DATA_SCRAPED)],
            method=HashingMethod.RGBA,
            root_dir=DIR_DATA_SCRAPED,
            verbose=True
        )

        # Assert
        detect_dups = []
        for dup_imgs in detect_dups_dict.values():
            for dup_img in dup_imgs:
                detect_dups.append(os.path.basename(dup_img.path))
        self.maxDiff = None
        self.assertCountEqual(test_dups, detect_dups)


if __name__ == '__main__':
    unittest.main()
