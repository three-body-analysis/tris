import unittest
from tqdm import tqdm
from glob import glob
import pandas as pd
import numpy as np

from tris.io import read_df, read_csv, read_excel, read_json

import warnings

warnings.filterwarnings("ignore")


class DataReadTestCase(unittest.TestCase):
    def test_read_df(self):
        df = pd.read_csv("tests/sample_data/processed.csv")
        df_copy = pd.read_csv("tests/sample_data/processed.csv")

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

    def test_excel(self):
        df = pd.read_csv("tests/sample_data/processed.csv")

        df_test_index_index_index = read_excel("tests/sample_data/processed.xlsx", 0, 1, 0)
        self.assertTrue(df.equals(df_test_index_index_index), "Index-Index-Index Read Test (identity) Failed")

        df_test_index_index_name = read_excel("tests/sample_data/processed.xlsx", 0, 1, "processed")
        self.assertTrue(df.equals(df_test_index_index_name), "Index-Index-Name Read Test (identity) Failed")

        df_test_index_name_index = read_excel("tests/sample_data/processed.xlsx", 0, "flux", 0)
        self.assertTrue(df.equals(df_test_index_name_index), "Index-Name-Index Read Test (identity) Failed")

        df_test_index_name_name = read_excel("tests/sample_data/processed.xlsx", 0, "flux", "processed")
        self.assertTrue(df.equals(df_test_index_name_name), "Index-Name-Name Read Test (identity) Failed")

        df_test_name_index_index = read_excel("tests/sample_data/processed.xlsx", "time", 1, 0)
        self.assertTrue(df.equals(df_test_name_index_index), "Name-Index-Index Read Test (identity) Failed")

        df_test_name_index_name = read_excel("tests/sample_data/processed.xlsx", "time", 1, "processed")
        self.assertTrue(df.equals(df_test_name_index_name), "Name-Index-Name Read Test (identity) Failed")

        df_test_name_name_index = read_excel("tests/sample_data/processed.xlsx", "time", "flux", 0)
        self.assertTrue(df.equals(df_test_name_name_index), "Name-Name-Index Read Test (identity) Failed")

        df_test_name_name_name = read_excel("tests/sample_data/processed.xlsx", "time", "flux", "processed")
        self.assertTrue(df.equals(df_test_name_name_name), "Name-Name-Name Read Test (identity) Failed")

        df_test_index_index_index = read_excel("tests/sample_data/manipulated.xlsx", 1, 3, 0)
        self.assertTrue(df.equals(df_test_index_index_index), "Index-Index-Index Read Test (identity) Failed")

        df_test_index_index_name = read_excel("tests/sample_data/manipulated.xlsx", 1, 3, "manipulated")
        self.assertTrue(df.equals(df_test_index_index_name), "Index-Index-Name Read Test (identity) Failed")

        df_test_index_name_index = read_excel("tests/sample_data/manipulated.xlsx", 1, "flux", 0)
        self.assertTrue(df.equals(df_test_index_name_index), "Index-Name-Index Read Test (identity) Failed")

        df_test_index_name_name = read_excel("tests/sample_data/manipulated.xlsx", 1, "flux", "manipulated")
        self.assertTrue(df.equals(df_test_index_name_name), "Index-Name-Name Read Test (identity) Failed")

        df_test_name_index_index = read_excel("tests/sample_data/manipulated.xlsx", "time", 3, 0)
        self.assertTrue(df.equals(df_test_name_index_index), "Name-Index-Index Read Test (identity) Failed")

        df_test_name_index_name = read_excel("tests/sample_data/manipulated.xlsx", "time", 3, "manipulated")
        self.assertTrue(df.equals(df_test_name_index_name), "Name-Index-Name Read Test (identity) Failed")

        df_test_name_name_index = read_excel("tests/sample_data/manipulated.xlsx", "time", "flux", 0)
        self.assertTrue(df.equals(df_test_name_name_index), "Name-Name-Index Read Test (identity) Failed")

        df_test_name_name_name = read_excel("tests/sample_data/manipulated.xlsx", "time", "flux", "manipulated")
        self.assertTrue(df.equals(df_test_name_name_name), "Name-Name-Name Read Test (identity) Failed")

    def test_json(self):
        df = pd.read_csv("tests/sample_data/processed.csv")

        df_test_full_index = read_json("tests/sample_data/processed.json", 0, 1)
        self.assertTrue(df.equals(df_test_full_index), "Full Index Read Test (identity) Failed")

        df_test_full_name = read_json("tests/sample_data/processed.json", "time", "flux")
        self.assertTrue(df.equals(df_test_full_name), "Full Name Read Test (identity) Failed")

        df_test_name_index = read_json("tests/sample_data/processed.json", "time", 1)
        self.assertTrue(df.equals(df_test_name_index), "Name, Index Read Test (identity) Failed")

        df_test_index_name = read_json("tests/sample_data/processed.json", 0, "flux")
        self.assertTrue(df.equals(df_test_index_name), "Index, Name Read Test (identity) Failed")


if __name__ == '__main__':
    unittest.main()
