from utilities.filehandler import FileHandler
from utilities.graphing import *
from pprint import pprint


class Account:
    def __init__(self):
        self.initial_capital = 1000
        self.equity = self.initial_capital

    def update_equity(self, amount):
        self.equity += amount

    def reset_equity(self):
        self.equity = self.initial_capital


class RiskModel:
    def __init__(self, account):
        self.position_sizing = 1
        self.safety_margin = 100
        self.account = account

    def get_position_size(self, asset_price):
        return (self.position_sizing * (self.account.equity / asset_price)) - \
               (self.safety_margin / asset_price)


class ExecutionModel:
    def __init__(self, account):
        self.account = account
        self.risk_model = RiskModel(account)
        # backtesting vars
        self.open_equity = 0
        self.open_amount = 0

    @staticmethod
    def limit_buy(price, currency, time_limit):
        pass

    @staticmethod
    def limit_sell(price, currency, time_limit):
        pass

    def backtest_buy(self, price, index, hist_array):
        info = {}
        self.open_amount = self.risk_model.get_position_size(price)
        self.open_equity = price * self.open_amount
        info.update({'open_amount': self.open_amount,
                     'open_price': price,
                     'open_equity': self.open_equity,
                     'open_index': index})
        hist_array.append(info)

    def backtest_sell(self, price, index, hist_array):
        info = {}
        info.update({'close_amount': self.open_amount,
                     'close_equity': price * self.open_amount,
                     'close_price': price,
                     'price_delta': (price * self.open_amount) - self.open_equity,
                     'close_index': index})
        self.account.update_equity(info.get('price_delta'))
        hist_array.append(info)


class Algorithm:
    def backtest_action(self, index, data, hist_array):
        raise NotImplementedError

    def action(self):
        raise NotImplementedError


class BacktestModel:

    def __init__(self, algorithm, account):
        self.algorithm = algorithm
        self.account = account

    def backtest(self, currency):
        data = FileHandler.read_from_file(FileHandler.get_filestring(currency))
        print(self.account.equity)
        for i in range(len(data)):
            self.algorithm.backtest_action(i, data)
        print(self.account.equity)
        self.account.reset_equity()

    def interactive_backtest(self, currency):
        data = FileHandler.read_from_file(FileHandler.get_filestring(currency))
        hist_array = []
        for i in range(len(data)):
            self.algorithm.backtest_action(i, data, hist_array)

        x = hist_array
        moving_average_full_graph(data, 10, 20, hist_array)

    def full_backest(self, universe):
        results_dict = {}
        for currency in universe:
            self.backtest(currency)
            results_dict.update({currency: self.account.equity})
        pprint(results_dict)
