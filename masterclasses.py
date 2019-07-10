from utilities.filehandler import FileHandler
from utilities.graphing import *
from pprint import pprint


class Account:
    equity = 0
    cash = 0
    # equity = cash + market value of all active holdings
    # QUANTITY = AMOUNT IN NATIVE CURRENCY (ETH, BTC, ETC...)
    # MKT_VALUE = WHAT THAT QUANTITY IS WORTH IN USD AT A GIVEN TIME

    holdings = {}
    # {'DOGE-USD':  {'cost_basis': 100000,
    #               'mkt_value': 99999,
    #              'quantity': 12345}
    #                               }

    def __init__(self):
        self.initial_capital = 1000
        Account.equity = self.initial_capital
        Account.cash = Account.equity
        Account.holdings.update({'ETH-USD': {'cost_basis': 0,
                                             'mkt_value': 0,
                                             'quantity': 0}
                                 })  # very temporary

    @staticmethod
    def update_mkt(currency, price):
        c = Account.holdings.get(currency)
        c.update({'mkt_value': price * c['quantity']})

    @staticmethod
    def update_equity():
        sum_mkt = 0
        if len(Account.holdings) > 0:
            for k, v in Account.holdings.items():
                sum_mkt += v['mkt_value']

        Account.equity = Account.cash + sum_mkt


class RiskModel:
    position_sizing = .5

    @staticmethod
    def get_position_size(signal_strength):
        # return signal_strength * (RiskModel.position_sizing * Account.equity)
        return 5  # FUCK YOU MR. FUNCTION


class ExecutionModel:

    @staticmethod
    def limit_buy(price, currency, time_limit):
        pass

    @staticmethod
    def limit_sell(price, currency, time_limit):
        pass

    @staticmethod
    def backtest_buy(signal, price):
        c = Account.holdings.get(signal['currency'])
        q1 = c.get('quantity')
        q2 = signal['quantity']
        c.update({'quantity': q1 + q2})
        Account.cash -= q2 * price

    @staticmethod
    def backtest_sell(signal, price):
        c = Account.holdings.get(signal['currency'])
        q1 = c.get('quantity')
        q2 = signal['quantity']
        if q2 < q1:
            tq = q1 - q2
        else:
            tq = q1

        c.update({'quantity': tq})
        Account.cash += tq * price


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
    def execute_on_signal(signal, price):
        # feeds the signal into execution model to simulate buying and selling
        if signal['action'] == 'buy':
            ExecutionModel.backtest_buy(signal, price)
        elif signal['action'] == 'sell':
            ExecutionModel.backtest_sell(signal, price)
        else:
            signal.update({'quantity': 0})

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
        drawdown_stats = {'ddp': max_dd_percent,
                          'ddl': max_dd_length,
                          'gmax_idx': gmax_idx,
                          'gmin_idx': gmin_idx}

        return drawdown_stats

    def generate_backtest(self, currency):
        data = pd.DataFrame(FileHandler.read_from_file(FileHandler.get_filestring(currency)))
        backtest_data = {}
        signal_data = []
        account_equity = []
        initial_equity = Account.equity
        equity = 0

        for i in range(len(data)):
            sma20_series = Technicals.pandas_sma(20, data)
            sma50_series = Technicals.pandas_sma(50, data)
            sma20 = float(sma20_series[i])
            sma50 = float(sma50_series[i])
            signal = self.algorithm.backtest_action(short_sma=sma20,
                                                    long_sma=sma50)

            signal.update({'currency': currency})
            self.update_quantity(signal)
            self.execute_on_signal(signal, float(data.at[i, 'close']))

            Account.update_mkt(currency=currency,
                               price=float(data.at[i, 'close']))
            Account.update_equity()
            equity = Account.equity
            signal_data.append(signal)
            account_equity.append(equity)

        dd_stats = self.calc_drawdown(account_equity)
        backtest_data.update({'signal_data': signal_data,
                              'account_equity': account_equity,
                              'gmax_idx': dd_stats['gmax_idx'],
                              'gmin_idx': dd_stats['gmin_idx'],
                              })
        profit = round(equity - initial_equity, 2)

        backtest_stats = {
            'initial equity': '${}'.format(initial_equity),
            'profit': '${}'.format(profit),
            'return': '{}%'.format(round(100 * (profit / initial_equity), 2)),
            'max. drawdown': '{}%'.format(round(dd_stats['ddp'], 2)),
            'longest drawdown': '{} candles'.format(dd_stats['ddl'])
        }
        return backtest_data, backtest_stats

    def visualize_backtest(self, currency):
        data = FileHandler.read_from_file(FileHandler.get_filestring(currency))
        backtest_data, backtest_stats = self.generate_backtest(currency)

        moving_average_full_graph(data=data,
                                  short_period=20,
                                  long_period=50,
                                  backtest_data=backtest_data,
                                  backtest_stats=backtest_stats)

    # def full_backest(self, universe):
    #     results_dict = {}
    #     for currency in universe:
    #         self.visualize_backtest(currency)
    #         results_dict.update({currency: self.account.equity})
    #     pprint(results_dict)
