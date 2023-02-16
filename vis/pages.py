import matplotlib.pyplot as pl
import numpy as np
import pandas as pd


class PagesPerDate():
    def __init__(self, dataset):
        self.df = dataset

        self.fig, self.ax = pl.subplots(1)

    def per_month(self, no_of_months=12, culminate=False):
        subset = self.df[['Pages Read', 'Ended Reading On']]

        subset = subset[~pd.isna(subset['Ended Reading On'])]

        dataset = subset.to_numpy()

        months = []

        for item in dataset[:, 1]:
            month_year = item[:7]
            if not month_year in months and (month_year.startswith('2022') or month_year.startswith('2023')):
                months.append(month_year)

        data = dict(zip(months, [0 for item in range(len(months))]))

        for row in dataset:
            if not row[1][:7] in months:
                continue
            data[row[1][:7]] += row[0]

        lists = sorted(data.items())
        x, y = zip(*lists)

        if culminate:
            y = [y[-no_of_months]] + [sum(y[-no_of_months:n]) for n in range(len(y) - no_of_months, len(y))]

        if no_of_months > len(x):
            no_of_months = len(x)

        self.fig.autofmt_xdate()
        self.ax.set_xlabel('Month')
        self.ax.set_ylabel('No. of Pages')

        self._visualize(x[-no_of_months:], y[-no_of_months:],
                        'Pages Read', f'Pages read in the last {no_of_months} months', no_of_months)

    def per_week(self, no_of_weeks=52, culminate=False):
        subset = self.df[['Pages Read', 'Ended Reading On']]

        subset = subset[~pd.isna(subset['Ended Reading On'])]

        dataset = subset.to_numpy()  #

        weeks = []
        for item in dataset[:, 1]:
            month_year = item[:7]
            if month_year.startswith('2022') or month_year.startswith('2023'):
                year_kw = item[:4] + '-' + str(pd.to_datetime(item).isocalendar().week).rjust(2, '0')
                if not year_kw in weeks:
                    weeks.append(year_kw)

        data = dict(zip(weeks, [0 for item in range(len(weeks))]))

        for row in dataset:
            year_kw = row[1][:4] + '-' + str(pd.to_datetime(row[1]).isocalendar().week).rjust(2, '0')
            if not year_kw in weeks:
                continue
            data[year_kw] += row[0]

        lists = sorted(data.items())
        x, y = zip(*lists)

        if culminate:
            y = [y[-no_of_weeks]] + [sum(y[-no_of_weeks:n]) for n in range(len(y) - no_of_weeks, len(y))]

        self.ax.set_xlabel('Calendar Week')
        self.ax.set_ylabel('No. of Pages')

        self._visualize(x[-no_of_weeks:], y[-no_of_weeks:],
                        'Pages Read', f'Pages read in the last {no_of_weeks} weeks.', no_of_weeks)

    def per_week_culm(self, no_of_weeks=52):
        self.per_week(no_of_weeks, culminate=True)

    def per_month_culm(self, no_of_month=52):
        self.per_month(no_of_month, culminate=True)

    def _visualize(self, x, y, label, title, no):
        pl.plot(x, y, label=label)
        pl.xlim(x[0], x[-1])
        pl.ylim(0, np.amax(y) + 500)

        idx = 1
        if no > 8:
            idx = int(no / 10) + 1
        for n, label in enumerate(self.ax.xaxis.get_ticklabels()):
            if not n % idx == 0:
                label.set_visible(False)

        pl.grid()
        pl.legend()
        pl.title(title)
        pl.show()


if __name__ == '__main__':
    from load import pand

    df = pand.load_csv_pandas('../data/Bookshelf-2023-02-04.csv')

    ppd = PagesPerDate(df)

    ppd.per_week_culm(10)
