import pandas as pd
import matplotlib.pyplot as plt
from mpl_finance import candlestick2_ochl
import numpy as np


class GraphHandler:
    @staticmethod
    def add_titlebox(ax, text):
        ax.text(.55, .8, text,
                horizontalalignment='center',
                transform=ax.transAxes,
                bbox=dict(facecolor='white', alpha=0.6),
                fontsize=12.5)
        return ax

    @staticmethod
    def full_graph(data):
        dataset = pd.DataFrame(data=data)
        # dataset = pd.DataFrame(data=data)
        gridsize = (4, 2)
        ax1 = plt.subplot2grid(gridsize, (0, 0), colspan=2, rowspan=2)
        ax2 = plt.subplot2grid(gridsize, (2, 0), colspan=2)
        ax3 = plt.subplot2grid(gridsize, (3, 0))
        ax4 = plt.subplot2grid(gridsize, (3, 1))
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Price')
        ax1.grid()
        candlestick2_ochl(ax=ax1, opens=dataset['open'], closes=dataset['close'],
                          highs=dataset['high'], lows=dataset['low'],
                          width=1, alpha=1, colorup='green', colordown='red',)

        sma_50 = dataset['close'].rolling(10).mean()
        sma_20 = dataset['close'].rolling(20).mean()
        sma_delta = sma_50 - sma_20

        sma_delta.plot(ax=ax2)
        sma_50.plot(ax=ax1)
        sma_20.plot(ax=ax1)

        plt.show()
