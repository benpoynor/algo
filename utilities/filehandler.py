import pandas as pd
import settings
import os
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
        prefix = settings.DATA_PATH
        path = '{}{}_{}.csv'.format(
            prefix, currency.replace('-', '_'), timeframe)
        return pd.read_csv(path)

    @staticmethod
    def get_filestring(currency_str):
        return 'data/{}_daily'.format(currency_str.replace('-', '_'))
