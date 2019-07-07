from utilities.filehandler import FileHandler
from utilities.graphing import *
from pprint import pprint


class Account:
    equity = 0

    def __init__(self):
        self.initial_capital = 1000
        Account.equity = self.initial_capital


class RiskModel:
    position_sizing = .5

    @staticmethod
    def get_position_size(signal_strength):
        return signal_strength * (RiskModel.position_sizing * Account.equity)


class ExecutionModel:

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

    def __init__(self, algorithm):
        self.algorithm = algorithm

    @staticmethod
    def debug(backtest_data):
        for idx, val in enumerate(backtest_data):
            if val['action'] == 'buy':
                # print('bought at {}'.format(data.at[idx, 'close']))
                pass
            elif val['action'] == 'sell':
                # print('sold at {}'.format(data.at[idx, 'close']))
                pass

    @staticmethod
    def update_quantity(signal):
        # feeds signal into risk model to get position sizing
        signal.update({'quantity': RiskModel.get_position_size(signal['signal_str'])})

    @staticmethod
    def execute_on_signal(signal):
        # feeds the signal into execution model to simulate buying and selling
        if signal['action'] == 'buy':
            ExecutionModel.backtest_buy(signal)
        elif signal['action'] == 'sell':
            ExecutionModel.backtest_sell(signal)
        else:
            signal.update({'quantity': 0})

    def generate_backtest(self, currency):
        data = pd.DataFrame(FileHandler.read_from_file(FileHandler.get_filestring(currency)))
        backtest_data = []
        account_equity = []

        for i in range(len(data)):
            sma20_series = Technicals.pandas_sma(20, data)
            sma50_series = Technicals.pandas_sma(50, data)
            sma20 = float(sma20_series[i])
            sma50 = float(sma50_series[i])
            signal = self.algorithm.backtest_action(short_sma=sma20,
                                                    long_sma=sma50)

            self.update_quantity(signal)
            self.execute_on_signal(signal)
            equity = Account.equity

            backtest_data.append(signal)
            account_equity.append(equity)

        return backtest_data, account_equity

    def visualize_backtest(self, currency):
        data = FileHandler.read_from_file(FileHandler.get_filestring(currency))
        backtest_data, account_equity = self.generate_backtest(currency)

        moving_average_full_graph(data=data,
                                  short_period=20,
                                  long_period=50,
                                  backtest_data=backtest_data,
                                  account_equity=account_equity)

    # def full_backest(self, universe):
    #     results_dict = {}
    #     for currency in universe:
    #         self.visualize_backtest(currency)
    #         results_dict.update({currency: self.account.equity})
    #     pprint(results_dict)
