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

    @staticmethod
    def backtest_buy(signal):
        signal.update({'quantity': 100})
        # arbitrary for now

    @staticmethod
    def backtest_sell(signal):
        signal.update({'quantity': 100})
        # arbitrary for now


class Algorithm:
    # index here just means date
    def backtest_action(self, data, index):
        raise NotImplementedError

    def action(self):
        raise NotImplementedError


class BacktestModel:

    def __init__(self, algorithm, account, execution_model, risk_model):
        self.algorithm = algorithm
        self.account = account
        self.execution_model = execution_model
        self.risk_model = risk_model

    def generate_backtest(self, currency):
        data = pd.DataFrame(FileHandler.read_from_file(FileHandler.get_filestring(currency)))
        backtest_data = []

        for i in range(len(data)):
            sma20_series = Technicals.pandas_sma(20, data)
            sma50_series = Technicals.pandas_sma(50, data)
            sma20 = float(sma20_series[i])
            sma50 = float(sma50_series[i])
            signal = self.algorithm.backtest_action(short_sma=sma20,
                                                    long_sma=sma50)
            if signal['action'] == 'buy':
                self.execution_model.backtest_buy(signal)
            elif signal['action'] == 'sell':
                self.execution_model.backtest_sell(signal)
            else:
                signal.update({'quantity': 0})

            backtest_data.append(signal)

        for idx, val in enumerate(backtest_data):
            if val['action'] == 'buy':
                print('bought at {}'.format(data.at[idx, 'close']))
            elif val['action'] == 'sell':
                print('sold at {}'.format(data.at[idx, 'close']))

        return backtest_data

    def execute_backtest(self, currency):
        data = FileHandler.read_from_file(FileHandler.get_filestring(currency))
        backtest_data = self.generate_backtest(currency)

        moving_average_full_graph(data=data,
                                  short_period=20,
                                  long_period=50,
                                  backtest_data=backtest_data)

    def full_backest(self, universe):
        results_dict = {}
        for currency in universe:
            self.execute_backtest(currency)
            results_dict.update({currency: self.account.equity})
        pprint(results_dict)
