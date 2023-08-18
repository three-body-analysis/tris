import unittest
from tqdm import tqdm
from glob import glob

from pipeline.preproc import read

import warnings

warnings.filterwarnings("ignore")


class DataReadCase(unittest.TestCase):

    def test_all(self):
        all_systems = glob("../data/combined/*.fits")
        for filename in tqdm(all_systems):
            system = filename.split("\\")[-1].split('.')[0]
            df = read(filename)
            self.assertEqual(
                tuple(df.columns), ("time", "flux"),
                f"Columns don't match for {system}: Expected ('time', 'flux'), found {tuple(df.columns)}"
            )


if __name__ == '__main__':
    unittest.main()
