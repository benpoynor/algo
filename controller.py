from algos import sma_algo
from masterclasses import Backtest
from utilities.filehandler import FileHandler
from utilities.datascraper import DataScraper
from settings import BACKTEST_CURRENCIES as BC
import os


def run_backtest():
    a = sma_algo.MovingAverageAlgo()
    d = FileHandler.read_from_file('data/testfile.csv')
    Backtest(d, a, 'BTC-USD')


def get_filestring(currency_str):
    return 'data/{}_daily'.format(currency_str.replace('-', '_'))


def run_all_backtests():
    for currency in BC:
        a = sma_algo.MovingAverageAlgo()
        d = FileHandler.read_from_file(get_filestring(currency))
        Backtest(d, a, currency)


def create_data():
    for currency in BC:
        filestring = get_filestring(currency)
        data = DataScraper.get_yahoo_pricehist(currency, '2017-01-01', '2019-06-15')
        FileHandler.write_to_file(filestring, data)
        size = os.path.getsize(filestring) / 1000
        printstring = 'file written : {}, ({} kb)'.format(filestring, size)
        print(printstring)


if __name__ == "__main__":
    run_all_backtests()
