from algos import sma_algo
from masterclasses import Backtest
from utilities.filehandler import FileHandler
from utilities.datascraper import DataScraper
from settings import BACKTEST_CURRENCIES as BC
import os


def run_all_backtests():
    for currency in BC:
        a = sma_algo.MovingAverageAlgo()
        d = FileHandler.read_from_file(FileHandler.get_filestring(currency))
        b = Backtest(d, a, currency)
        print(b.get_results())


def create_data():
    for currency in BC:
        filestring = FileHandler.get_filestring(currency)
        data = DataScraper.get_yahoo_pricehist(currency, '2017-01-01', '2019-06-15')
        FileHandler.write_to_file(filestring, data)
        size = os.path.getsize(filestring) / 1000
        printstring = 'file written : {}, ({} kb)'.format(filestring, size)
        print(printstring)


if __name__ == "__main__":
    run_all_backtests()
