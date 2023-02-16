import numpy as np
import pandas as pd


def load_csv_pandas(fp):
    data = pd.read_csv(fp)

    return data


if __name__ == '__main__':
    load_csv_pandas('../data/Bookshelf-2023-02-04.csv')