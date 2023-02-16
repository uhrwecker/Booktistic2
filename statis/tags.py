import numpy as np
import pandas as pd


class TagStatistics():
    def __init__(self, dataset):
        self.df = dataset

    def top_3(self, scale='W', no=12, unique=True):
        subset = self.df[['Tags', 'Ended Reading On', 'Pages Read']]

        subset = subset[~pd.isna(subset['Ended Reading On'])]
        subset = subset[~pd.isna(subset['Tags'])]

        subset['Ended Reading On'] = pd.to_datetime(subset['Ended Reading On'])
        subset.sort_values(by='Ended Reading On', inplace=True)

        subset = subset.set_index(['Ended Reading On'])
        subset = subset.last(f'{no}{scale}')

        data = subset['Tags'].to_numpy()
        if unique:
            data = [item.split(',') for item in data]
            data = [item for sublist in data for item in sublist]
        else:
            data = data.tolist()

        tags = list(set(data))

        df = pd.DataFrame({'Tags': list(set(data)), 'Count': [data.count(item) for item in list(set(data))],
                           'Pages Read': [sum([subset['Pages Read'][n] for n in range(len(subset['Pages Read'])) if tag in subset['Tags'][n]]) for tag in tags]})
        df.sort_values(by='Count', ascending=False, inplace=True)

        return df[:3]


if __name__ == '__main__':
    from load import pand

    df = pand.load_csv_pandas('../data/Bookshelf-2023-02-04.csv')

    ts = TagStatistics(df)

    print(ts.top_3(scale='M', no=8))
