from yahoofinancials import YahooFinancials
from utilities.filehandler import FileHandler
from settings import BACKTEST_CURRENCIES as UNIVERSE
import os


class DataScraper:
    @staticmethod
    def get_yahoo_pricehist(ticker, startdate, enddate):
        yf = YahooFinancials(ticker)
        hsp = yf.get_historical_price_data(startdate, enddate, 'daily')
        return hsp[ticker]['prices']

    @staticmethod
    def create_data():
        for currency in UNIVERSE:
            filestring = FileHandler.get_filestring(currency)
            data = DataScraper.get_yahoo_pricehist(currency, '2017-01-01', '2019-06-15')
            FileHandler.write_to_file(filestring, data)
            size = os.path.getsize(filestring) / 1000
            printstring = 'file written : {}, ({} kb)'.format(filestring, size)
            print(printstring)
