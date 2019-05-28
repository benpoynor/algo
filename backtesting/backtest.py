import matplotlib.pyplot as plt
import pandas as pd
from mpl_finance import candlestick2_ochl, volume_overlay2
try:
    import backtesting.datacontroller as dc
except ImportError:
    import datacontroller as dc


class Backtest:
    dataset = None

    def __init__(self, ds):
        Backtest.dataset = pd.DataFrame(data=ds)

    def graph(self):
        fig, ax1 = plt.subplots()
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Price')
        ax2 = ax1.twinx()
        ax2.set_ylabel('Volume')
        candlestick2_ochl(ax=ax1,
                          opens=Backtest.dataset['open'],
                          closes=Backtest.dataset['close'],
                          highs=Backtest.dataset['high'],
                          lows=Backtest.dataset['low'],
                          width=1,
                          colorup='green',
                          colordown='red',
                         )
        volume_overlay2(ax=ax2,
                        closes=Backtest.dataset['close'],
                        volumes=Backtest.dataset['volume'],
                        width=1,
                        alpha=.5,
                        colorup='green',
                        colordown='red')
        plt.show()


raw_data = dc.get_debug_pricehist('BTC-USD', '2019-04-01', '2019-05-26')
bt = Backtest(raw_data)
bt.graph()
