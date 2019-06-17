from algos import sma_algo
from masterclasses import Backtest
from utilities.filehandler import FileHandler


def run_backtest():
    a = sma_algo.MovingAverageAlgo()
    d = FileHandler.read_from_file('data/testfile.csv')
    b = Backtest(d, a)


def create_data():
    pass


if __name__ == "__main__":
    run_backtest()
