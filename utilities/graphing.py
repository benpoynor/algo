import pandas as pd
import matplotlib.pyplot as plt
from mpl_finance import candlestick2_ochl


def graph(ds):
    dataset = pd.DataFrame(data=ds)
    fig, ax1 = plt.subplots()
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Price')

    candlestick2_ochl(ax=ax1,
                      opens=dataset['open'],
                      closes=dataset['close'],
                      highs=dataset['high'],
                      lows=dataset['low'],
                      width=1,
                      alpha=1,
                      colorup='green',
                      colordown='red',
                     )
    plt.show()
