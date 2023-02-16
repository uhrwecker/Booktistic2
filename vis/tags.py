import numpy as np
import pandas as pd
import matplotlib.pyplot as pl
from datetime import date
from dateutil.relativedelta import relativedelta


class PagesPerTag():
    def __init__(self, dataset):
        self.df = dataset

        self.fig = pl.figure(figsize=(15, 8))

    def top_3(self, scale='W', no=12, unique=True, culminate=False):
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

        for tag in tags:
            if scale == 'W':
                x0 = date.today() + relativedelta(weeks=-no)
            elif scale == 'M':
                x0 = date.today() + relativedelta(months=-no)
                x0 = pd.to_datetime(f'{x0.year}-{x0.month}-01')
            else:
                raise KeyError

            x = pd.date_range(x0, freq=f'1{scale}', periods=no)
            df = subset[subset['Tags'].str.contains(tag)]

            if scale == 'W':
                y = [sum([df['Pages Read'][n] for n in range(len(df.index)) if
                          (df.index[n].month == dates.month and df.index[n].year == dates.year)]) for dates in x]
                title_scale = f'{no} weeks'
            elif scale == 'M':
                y = [sum([df['Pages Read'][n] for n in range(len(df.index)) if
                          (df.index[n].isocalendar().week == dates.isocalendar().week and df.index[n].year == dates.year)]) for dates in x]
                title_scale = f'{no} months'
            else:
                raise KeyError

            if culminate:
                y = np.cumsum(y)

            self._visualize(x, y, tag, title_scale)

        pl.show()

    def _visualize(self, x, y, tag, ts):
        pl.plot(x, y, label=tag)
        pl.xlim(x[0], x[-1])

        pl.title('Pages read per tag in the last ' + ts)
        pl.xlabel('Ended Reading On')
        pl.ylabel('No. of Pages')
        pl.legend()
        pl.grid()


if __name__ == '__main__':
    from load import pand

    df = pand.load_csv_pandas('../data/Bookshelf-2023-02-04.csv')

    ts = PagesPerTag(df)

    print(ts.top_3(scale='W', no=2, culminate=True))
