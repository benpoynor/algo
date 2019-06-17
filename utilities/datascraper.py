from yahoofinancials import YahooFinancials


class DataScraper:
    @staticmethod
    def get_yahoo_pricehist(ticker, startdate, enddate):
        yf = YahooFinancials(ticker)
        hsp = yf.get_historical_price_data(startdate, enddate, 'daily')
        return hsp[ticker]['prices']
