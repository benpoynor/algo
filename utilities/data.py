from yahoofinancials import YahooFinancials
import csv
import pandas as pd


def get_yahoo_pricehist(ticker, startdate, enddate):
    yf = YahooFinancials(ticker)
    hsp = yf.get_historical_price_data(startdate, enddate, 'daily')
    return hsp[ticker]['prices']


def sma(period, dataset, index):
    ma = 0
    for i in range(period):
        if index - i > 0:
            ma += float(dataset[index - i]['close'])
        else:
            return 0
    return ma/period


def write_to_file(path, data):
    with open(path, mode='w+') as csvfile:
        datawriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        datawriter.writerow(list(data[0].keys()))
        for entry in data:
            datawriter.writerow(list(entry.values()))


def read_from_file(path):
    with open(path) as csvfile:
        datareader = csv.DictReader(csvfile)
        csvdata = []
        for row in datareader:
            csvdata.append(row)

        return csvdata


def pandas_read_from_file(path):
    return pd.read_csv(path)


# d = get_yahoo_pricehist('BTC-USD', '2018-01-01', '2019-01-01')
# write_to_file('data/testfile.csv', d)
#
# x = read_from_file('data/testfile.csv')
# print(x)
