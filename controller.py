from algos import sma_algo
from masterclasses import Backtest
from utilities import data
from datetime import datetime
if __name__ == "__main__":
    a = sma_algo.MovingAverageAlgo()
    d = data.x = data.read_from_file('data/testfile.csv')
    b = Backtest(d, a)
