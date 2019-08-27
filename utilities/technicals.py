import pandas as pd
import settings


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
    def calc_derivative(series: pd.Series) -> pd.Series:
        dxdys = []
        for i in range(series.index[0] + 1, series.index[-1]):
            dy = series[i] - series[i - 1]
            dxdys.append(dy/2)
        return pd.Series(dxdys)

    @staticmethod
    def calc_drawdown(equity_history):  # i'm sure there's a better way but i don't care
        highest_high = equity_history[0]
        lowest_low = equity_history[0]
        dip_length = 0
        longest_dip = 0
        largest_dip = 0
        gmax_idx = 0
        gmin_idx = 0
        for idx, val in enumerate(equity_history):
            if val > highest_high:
                highest_high = val
                lowest_low = val
                dip_length = 0
                gmax_idx = idx
            else:
                dip_length += 1
            if val < lowest_low:
                lowest_low = val
                gmin_idx = idx
            if dip_length > longest_dip:
                longest_dip = dip_length
            dip_size = highest_high - lowest_low
            if dip_size > largest_dip:
                largest_dip = dip_size

        max_dd_percent = 100 * ((highest_high - lowest_low) / highest_high)
        max_dd_length = longest_dip
        drawdown_stats = {'drawdown_percent': max_dd_percent,
                          'drawdown_length': max_dd_length,
                          'gmax_idx': gmax_idx,
                          'gmin_idx': gmin_idx}

        return drawdown_stats

    @staticmethod
    def calc_sharpe(std: float,
                    annualized_return: float) -> float:
        rf = settings.RISK_FREE_RATE
        rp = annualized_return
        return float((rp - rf) / std)
