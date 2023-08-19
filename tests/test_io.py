import unittest
from tqdm import tqdm
from glob import glob
import pandas as pd
import numpy as np

from tris.io import read_df, read_csv

import warnings

warnings.filterwarnings("ignore")


class DataReadTestCase(unittest.TestCase):
    def test_read_df(self):
        df = pd.read_csv("tests/sample_data/processed.csv")
        df_copy = pd.read_csv("tests/sample_data/processed.csv")
        df_copy["col0"] = np.linspace(0, 1000, df.shape[0])
        df_copy[["col1", "col2"]] = np.random.random((df.shape[0], 2))

        df_copy = df_copy[["col0", "time", "col1", "flux", "col2"]]

        df_test_full_index = read_df(df, 0, 1)
        self.assertTrue(df.equals(df_test_full_index), "Full Index Read Test (identity) Failed")

        df_test_full_name = read_df(df, "time", "flux")
        self.assertTrue(df.equals(df_test_full_name), "Full Name Read Test (identity) Failed")

        df_test_name_index = read_df(df, "time", 1)
        self.assertTrue(df.equals(df_test_name_index), "Name, Index Read Test (identity) Failed")

        df_test_index_name = read_df(df, 0, "flux")
        self.assertTrue(df.equals(df_test_index_name), "Index, Name Read Test (identity) Failed")

        df_test_full_index = read_df(df_copy, 1, 3)
        self.assertTrue(df.equals(df_test_full_index), "Full Index Read Test (manipulated) Failed")

        df_test_full_name = read_df(df_copy, "time", "flux")
        self.assertTrue(df.equals(df_test_full_name), "Full Name Read Test (manipulated) Failed")

        df_test_name_index = read_df(df_copy, "time", 3)
        self.assertTrue(df.equals(df_test_name_index), "Name, Index Read Test (manipulated) Failed")

        df_test_index_name = read_df(df_copy, 1, "flux")
        self.assertTrue(df.equals(df_test_index_name), "Index, Name Read Test (manipulated) Failed")

    def test_csv(self):
        df = pd.read_csv("tests/sample_data/processed.csv")

        df_test_full_index = read_csv("tests/sample_data/processed.csv", 0, 1)
        self.assertTrue(df.equals(df_test_full_index), "Full Index Read Test (identity) Failed")

        df_test_full_name = read_csv("tests/sample_data/processed.csv", "time", "flux")
        self.assertTrue(df.equals(df_test_full_name), "Full Name Read Test (identity) Failed")

        df_test_name_index = read_csv("tests/sample_data/processed.csv", "time", 1)
        self.assertTrue(df.equals(df_test_name_index), "Name, Index Read Test (identity) Failed")

        df_test_index_name = read_csv("tests/sample_data/processed.csv", 0, "flux")
        self.assertTrue(df.equals(df_test_index_name), "Index, Name Read Test (identity) Failed")

        df_test_full_index = read_csv("tests/sample_data/manipulated.csv", 1, 3)
        self.assertTrue(df.equals(df_test_full_index), "Full Index Read Test (manipulated) Failed")

        df_test_full_name = read_csv("tests/sample_data/manipulated.csv", "time", "flux")
        self.assertTrue(df.equals(df_test_full_name), "Full Name Read Test (manipulated) Failed")

        df_test_name_index = read_csv("tests/sample_data/manipulated.csv", "time", 3)
        self.assertTrue(df.equals(df_test_name_index), "Name, Index Read Test (manipulated) Failed")

        df_test_index_name = read_csv("tests/sample_data/manipulated.csv", 1, "flux")
        self.assertTrue(df.equals(df_test_index_name), "Index, Name Read Test (manipulated) Failed")

    # def test_all(self):
    #     all_systems = glob("../data/combined/*.fits")
    #     for filename in tqdm(all_systems):
    #         system = filename.split("\\")[-1].split('.')[0]
    #         df = read(filename)
    #         self.assertEqual(
    #             tuple(df.columns), ("time", "flux"),
    #             f"Columns don't match for {system}: Expected ('time', 'flux'), found {tuple(df.columns)}"
    #         )


if __name__ == '__main__':
    unittest.main()
