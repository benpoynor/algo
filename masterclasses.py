from utilities.filehandler import FileHandler
from utilities.graphing import *
from settings import BACKTEST_CURRENCIES as UNIVERSE
from pprint import pprint
from threading import Thread


class Account:
    equity = 0
    cash = 0
    # equity = cash + market value of all active holdings
    # QUANTITY = AMOUNT IN NATIVE CURRENCY (ETH, BTC, ETC...)
    # MKT_VALUE = WHAT THAT QUANTITY IS WORTH IN USD AT A GIVEN TIME

    holdings = {}
    market_values = {}
    # {'DOGE-USD':  20}

    def __init__(self):
        self.initial_capital = 1000
        Account.equity = self.initial_capital
        Account.cash = Account.equity

        for c in UNIVERSE:
            Account.holdings.update({c: 0})
            Account.market_values.update({c: 0})

    @staticmethod
    def update_mkt(currency, price):
        c = Account.holdings.get(currency)
        c.update({'mkt_value': price * c['quantity']})

    @staticmethod
    def update_mkt_v2(signal):
        Account.market_values.update(
            {signal['currency']: signal['price'] * Account.holdings[signal['currency']]})

    @staticmethod
    def update_equity():
        sum_mkt = 0
        for k, v in Account.holdings.items():
            sum_mkt += v['mkt_value']

        Account.equity = Account.cash + sum_mkt

    @staticmethod
    def update_equity_v2():
        sum_mkt = 0
        for v in Account.market_values.values():
            sum_mkt += v

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
        c.update({'quantity': q1 - tq})
        Account.cash += tq * price

    @staticmethod
    def backtest_buy_v2(signal):
        q1 = Account.holdings.get(signal['currency'])
        q2 = signal['quantity']
        print('bought {} {} at {}. Total: '
              '{} -> Quantity of {}: {} --> {}'.format(signal['quantity'],
                                                       signal['currency'],
                                                       signal['price'],
                                                       signal['price'] * signal['quantity'],
                                                       signal['currency'],
                                                        q1, q1 + q2
                                                        ))
        Account.holdings[signal['currency']] = q1 + q2
        Account.cash -= q2 * signal['price']

    @staticmethod
    def backtest_sell_v2(signal):
        q1 = Account.holdings.get(signal['currency'])
        q2 = signal['quantity']
        if q2 < q1:
            tq = q1 - q2
        else:
            tq = q1
        print('sold {} {} at {}. Total: '
              '{} -> Quantity of {}: {} --> {}'.format(signal['quantity'],
                                                        signal['currency'],
                                                        signal['price'],
                                                        signal['price'] * signal['quantity'],
                                                        signal['currency'],
                                                        q1, q1 - tq
                                                        ))
        Account.holdings[signal['currency']] = q1 - tq
        Account.cash += tq * signal['price']


class Algorithm:
    # index here just means date
    def backtest_action(self, short_sma, long_sma, currency):
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
    def execute_on_signal_v2(signal):
        if signal['action'] == 'buy':
            ExecutionModel.backtest_buy_v2(signal)
        elif signal['action'] == 'sell':
            ExecutionModel.backtest_sell_v2(signal)
        else:
            signal.update({'quantity': 0})

    def generate_backtest(self, currency):  # OLD
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

        dd_stats = Technicals.calc_drawdown(account_equity)
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

    # def visualize_backtest(self, currency):
    #     data = FileHandler.read_from_file(FileHandler.get_filestring(currency))
    #     backtest_data, backtest_stats = self.generate_backtest(currency)
    #
    #     moving_average_full_graph(data=data,
    #                               short_period=20,
    #                               long_period=50,
    #                               backtest_data=backtest_data,
    #                               backtest_stats=backtest_stats)

    def get_individual_signal(self, currency, data, idx):
        sma20_series = Technicals.pandas_sma(20, data)
        sma50_series = Technicals.pandas_sma(50, data)
        sma20 = float(sma20_series[idx])
        sma50 = float(sma50_series[idx])
        signal = self.algorithm.backtest_action(short_sma=sma20,
                                                long_sma=sma50)

        signal.update({'currency': currency})
        signal.update({'price_at_signal': float(data.at[idx, 'close'])})
        self.update_quantity(signal)
        return signal

    # self.execute_on_signal_v2(signal)
    # Account.update_mkt_v2(signal)
    # Account.update_equity()
    # equity = Account.equity
    # account_equity.append(equity)

    def calc_backtest(self, universe):
        currencies = universe
        data_dict = {}
        equity_history = []

        for c in currencies:
            data = pd.DataFrame(FileHandler.read_from_file(FileHandler.get_filestring(c)))
            data_dict.update({c: data})

        for idx in range(len(data)):
            for c in currencies:
                sma20_series = Technicals.pandas_sma(20, data_dict[c])
                sma50_series = Technicals.pandas_sma(50, data_dict[c])
                sma20 = float(sma20_series[idx])
                sma50 = float(sma50_series[idx])
                signal = self.algorithm.backtest_action(short_sma=sma20,
                                                        long_sma=sma50,
                                                        currency=c)
                if signal['action'] == 'buy':
                    print('sma cross for {} @ idx: {}'.format(c, idx))
                signal.update({'currency': c})
                signal.update({'price': float(data_dict[c].at[idx, 'close'])})
                signal.update({'quantity': RiskModel.get_position_size(signal['signal_str'])})
                self.execute_on_signal_v2(signal)
                Account.update_mkt_v2(signal)
                Account.update_equity_v2()
            equity = Account.equity
            equity_history.append(equity)

        return pd.DataFrame(data=equity_history)

    def visualize_backtest(self, currency):
        # data = FileHandler.read_from_file(FileHandler.get_filestring(currency))
        # backtest_data, backtest_stats = self.generate_backtest(currency)

        equity_history = self.calc_backtest(UNIVERSE)

        debug_graph(equity_history)

        # moving_average_full_graph(data=data,
        #                           short_period=20,
        #                           long_period=50,
        #                           backtest_data=backtest_data,
        #                           backtest_stats=backtest_stats,
        #                           equity_history=equity_history)

    # def full_backest(self, universe):
    #     results_dict = {}
    #     for currency in universe:
    #         self.visualize_backtest(currency)
    #         results_dict.update({currency: self.account.equity})
    #     pprint(results_dict)
