import pandas as pd


class Technicals:

    @staticmethod
    def sma(period, dataset, index):
        ma = 0
        for i in range(period):
            if index - i > 0:
                ma += float(dataset[index - i]['close'])
            else:
                return 0
        return ma / period

    @staticmethod
    def pandas_sma(period, dataframe):
        return dataframe['close'].rolling(period).mean()

    @staticmethod
    def calc_derivative(series):
        dxdys = []
        for i in range(1, len(series) - 1):
            dy = series[i] - series[i - 1]
            dxdys.append(dy/2)
        return pd.Series(dxdys)
