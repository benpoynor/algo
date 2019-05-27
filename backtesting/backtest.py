import matplotlib.pyplot as plt
import pandas as pd
from mpl_finance import candlestick2_ochl
import backtesting.randomdata as rd
import backtesting.mkdata as mk
import backtesting.importdata as id


class Backtest:
    dataset = None

    def __init__(self, ds):
        Backtest.dataset = ds

    def graph(self):
        f1 = plt.subplot2grid((6, 4), (1, 0), rowspan=6, colspan=4)
        candlestick2_ochl(ax=f1,
                          opens=Backtest.dataset['open'],
                          closes=Backtest.dataset['close'],
                          highs=Backtest.dataset['high'],
                          lows=Backtest.dataset['low'],
                          width=1,
                          colorup='green',
                          colordown='red')
        plt.show()

x = mk.get_price_history('MSFT', '2019-01-01', '2019-02-01')
print(x.head())

pricedata = pd.DataFrame(data=rd.fake_data(30))
bt = Backtest(pricedata)
bt.graph()
