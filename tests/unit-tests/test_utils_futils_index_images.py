import unittest
import sys
import os
from os.path import dirname


sys.path.append(os.path.join(dirname(__file__) + '/../..', 'src/imdupes'))
sys.path.append(os.path.join(dirname(__file__) + '/../..', 'tests'))
from utils.futils import index_images
from tests import DIR_DATA_SCRAPED


class ExcludeFile(unittest.TestCase):
    def test(self):
        # Arrange

        # Act

        # Assert
        pass


if __name__ == '__main__':
    unittest.main()
