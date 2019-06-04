import matplotlib.pyplot as plt
import pprint
import pandas as pd
from mpl_finance import candlestick2_ochl
from yahoofinancials import YahooFinancials


def get_yahoo_pricehist(ticker, startdate, enddate):
    yf = YahooFinancials(ticker)
    hsp = yf.get_historical_price_data(startdate, enddate, 'daily')
    return hsp[ticker]['prices']


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


def sma(period, dataset, index):
    ma = 0
    for i in range(period):
        if index - i > 0:
            ma += dataset[index - i]['close']
        else:
            return None
    return ma/period


def ma_algo(dataset):

    for i in range(len(dataset)):
        if sma(20, dataset, i) > sma(50, dataset, i):
            dataset[i].update({'action': 'buy'})
        else:
            dataset[i].update({'action': 'sell'})

    pprint.pprint(dataset)


if __name__ == "__main__":
    raw_data = get_yahoo_pricehist('BTC-USD', '2018-10-01', '2019-05-26')
    ma_algo(raw_data)
