from algos import sma_algo
from masterclasses import Backtest
from utilities import data
from datetime import datetime
if __name__ == "__main__":
    a = sma_algo.MovingAverageAlgo()
    d = data.get_yahoo_pricehist('BTC', '2018-01-01', '2019-01-01')
    b = Backtest(data, a)