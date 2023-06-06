import unittest
import os

from detect_dup_imgs import detect_dup_imgs
from tests import DATA_DIR


def get_test_dups() -> list[str]:
    dups = set()

    for filename in os.listdir(DATA_DIR):
        filename_tokens = filename.split('_')
        if filename_tokens[0] == 'DUPLICATE':
            dups.add(filename)
            dups.add(filename_tokens[-1])

    return list(dups)


class Detect(unittest.TestCase):
    def test(self):
        test_dups = get_test_dups()

        detect_dups_dict = detect_dup_imgs(
            [os.path.join(DATA_DIR, img) for img in os.listdir(DATA_DIR)],
            root_dir=DATA_DIR,
            console_output=False, verbose=True
        )
        detect_dups = []
        for dup_imgs in detect_dups_dict.values():
            for dup_img in dup_imgs:
                detect_dups.append(os.path.basename(dup_img.path))

        self.assertCountEqual(test_dups, detect_dups)  # add assertion here


if __name__ == '__main__':
    unittest.main()
