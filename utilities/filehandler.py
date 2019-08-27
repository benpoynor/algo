import pandas as pd
import settings
import csv
import itertools


class FileHandler:
    @staticmethod
    def write_to_file(path, data):
        with open(path, mode='w+') as csvfile:
            datawriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            datawriter.writerow(list(data[0].keys()))
            for entry in data:
                datawriter.writerow(list(entry.values()))

    @staticmethod
    def read_from_file(path):
        # DEPRECIATED
        with open(path) as csvfile:
            datareader = csv.DictReader(csvfile)
            csvdata = []
            for row in datareader:
                csvdata.append(row)

            return csvdata

    @staticmethod
    def lower_first(iterator):
        return itertools.chain([next(iterator).lower()], iterator)

    @staticmethod
    def pandas_read_from_file(timeframe: str, currency: str) -> pd.DataFrame:
        r = range(200, 400)
        prefix = settings.DATA_PATH
        path = '{}{}_{}.csv'.format(
            prefix, currency.replace('-', '_'), timeframe)
        df = pd.read_csv(path)
        df_cropped = df.drop(df.index[:r[0]]).drop(df.index[r[-1]:])
        return df_cropped.reset_index(drop=True)

    @staticmethod
    def get_filestring(currency_str):
        return 'data/{}_daily'.format(currency_str.replace('-', '_'))
