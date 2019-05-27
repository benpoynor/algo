from yahoo_finance import Share
import pandas as pd


def make_price_history_file(ticker, startdate, enddate):
    sh = Share(ticker)
    data = pd.DataFrame(sh.get_historical(startdate, enddate))
    data.to_csv(index=False)
    print('file created!')


def get_price_history(ticker, startdate, enddate):
    sh = Share(ticker)
    data = pd.DataFrame(sh.get_historical(startdate, enddate))
    return data
