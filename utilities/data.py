from yahoofinancials import YahooFinancials


def get_yahoo_pricehist(ticker, startdate, enddate):
    yf = YahooFinancials(ticker)
    hsp = yf.get_historical_price_data(startdate, enddate, 'daily')
    return hsp[ticker]['prices']


def sma(period, dataset, index):
    ma = 0
    for i in range(period):
        if index - i > 0:
            ma += dataset[index - i]['close']
        else:
            return None
    return ma/period
