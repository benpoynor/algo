import pandas as pd
from utilities.technicals import Technicals
import settings


class MovingAverageAlgo:
    def __init__(self, data: dict):
        bc = settings.BACKTEST_CURRENCIES
        self.positions = {}
        self.sma_series_long = {}  # dict of pd.Series
        self.sma_series_short = {}  # dict of pd.Series

        for c in bc:
            self.sma_series_short.update({c: Technicals.pandas_sma(settings.SHORT_SMA_PERIOD, data[c])})
            self.sma_series_long.update({c: Technicals.pandas_sma(settings.LONG_SMA_PERIOD, data[c])})
            self.positions.update({c: False})

    def get_long_sma(self, c: str, idx: int) -> pd.Series:
        return self.sma_series_long[c][idx]

    def get_short_sma(self, c: str, idx: int) -> pd.Series:
        return self.sma_series_short[c][idx]

    def __str__(self):
        return 'Moving Average Algorithm V2'

    def backtest_action(self, currency: str, idx: int) -> dict:
        short_sma = self.get_short_sma(currency, idx)
        long_sma = self.get_long_sma(currency, idx)
        if short_sma > long_sma:
            if not self.positions.get(currency):
                # price = float(data[index].get('close'))
                # self.execution_model.backtest_buy(price, index)
                self.positions.update({currency: True})
                return {'action': 'buy',
                        'signal_str': 1,
                        'liquidate': False}
            else:
                return {'action': 'pass',
                        'signal_str': 1,
                        'liquidate': False}

        elif short_sma < long_sma:
            if self.positions.get(currency):
                # price = float(data[index].get('close'))
                # self.execution_model.backtest_sell(price, index)
                self.positions.update({currency: False})
                return {'action': 'sell',
                        'signal_str': 1,
                        'liquidate': False}
            else:
                return {'action': 'pass',
                        'signal_str': 1,
                        'liquidate': False}
        else:
            return {'action': 'pass',
                    'signal_str': 1,
                    'liquidate': False}

    def action(self):
        pass
