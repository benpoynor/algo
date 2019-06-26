from utilities.filehandler import FileHandler
from pprint import pprint


class RiskModel:
    def __init__(self):
        self.initial_capital = 1000
        self.position_sizing = 1
        self.safety_margin = 100

    def get_position_size(self, equity, asset_price):
        return (self.position_sizing * (equity / asset_price)) - (self.safety_margin / asset_price)


class ExecutionModel:
    def __init__(self):
        pass

    @staticmethod
    def limit_buy(price, currency, time_limit):
        pass

    @staticmethod
    def limit_sell(price, currency, time_limit):
        pass


class Algorithm:
    def __init__(self, risk_model):
        self.risk_model = risk_model

    def backtest_action(self, index, data, currency):
        raise NotImplementedError

    def action(self, index, data, currency):
        raise NotImplementedError


class BacktestModel:

    def __init__(self, universe, algorithm):
        self.universe = universe
        self.algorithm = algorithm

    @staticmethod
    def backtest(data, algorithm, currency):
        equity = algorithm.risk_model.initial_capital
        for i in range(len(data)):
            signal = algorithm.backtest_action(i, data, currency)
            if signal == 'buy':
                # fake buy
                pass
            elif signal == 'sell':
                # fake sell
                pass

        return equity

    def full_backest(self):
        results_dict = {}
        for currency in self.universe:
            d = FileHandler.read_from_file(FileHandler.get_filestring(currency))
            b = self.backtest(d, self.algorithm, currency)
            results_dict.update({currency: b})
        pprint(results_dict)
