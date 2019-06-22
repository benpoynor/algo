from utilities.filehandler import FileHandler
from pprint import pprint


class Algorithm:
    capital: float  # in USD
    initial_capital: float
    position_sizing: float  # as a percentage of total capital
    safety_margin: int  # in USD

    def __init__(self):
        self.position = Position()
        self.returns = 0.00
        self.initial_capital = self.capital

    def get_buy_amount(self, asset_price):
        return (self.position_sizing * (self.capital / asset_price)) - (self.safety_margin / asset_price)

    def update_returns(self):
        self.returns += self.position.returns

    def update_capital(self):
        self.capital += self.position.returns

    def reset_returns(self):
        self.position.returns = 0

    def action(self, index, data, currency):
        raise NotImplementedError


class Backtest:

    def __init__(self, data, algorithm, currency, verbose=False):
        for i in range(len(data)):
            algorithm.action(i, data, currency)
        # TODO: fix bug: position left open at end of backtest
        self.results = {}
        returnpercent = round((algorithm.returns / algorithm.initial_capital) * 100, 2)
        if verbose:
            ret = 'returns: {} ({}% return on initial capital of {}USD)'.format(algorithm.returns,
                                                                                returnpercent,
                                                                                algorithm.initial_capital)
            print(ret)

        self.results.update({'returns': algorithm.returns,
                             'returnpercent': returnpercent})

    def return_results(self):
        return self.results


class BacktestController:
    universe = []

    def __init__(self, universe, algorithm):
        self.universe = universe
        self.algorithm = algorithm

    def full_backest(self, verbose=False):
        results_dict = {}
        for currency in self.universe:
            d = FileHandler.read_from_file(FileHandler.get_filestring(currency))
            b = Backtest(d, self.algorithm, currency, verbose=verbose)
            results_dict.update({currency: b.return_results()})
        pprint(results_dict)


class Position:
    attributes = {}
    is_open: bool
    returns = 0
    open_cost_basis: float
    close_cost_basis: float

    def open(self, order_size,
             currency, current_price,
             current_time):
        # TODO: add different order types to position open and position close
        # later i need to add open_limit, open_market, open_large, open_small, etc...
        # for now though, this is OK, no reason to abstract so far into future yet...
        self.returns = 0
        self.attributes.update({
            'size': order_size,
            'currency': currency,
            'open_price': float(current_price),
            'open_time': current_time
        })
        # buy self.size of self.currency
        try:
            now = self.attributes['open_time'].strftime("%m/%d/%Y, %H:%M:%S")
        except AttributeError:
            now = self.attributes['open_time']
        self.open_cost_basis = self.attributes['size'] * self.attributes['open_price']

        ret = 'position opened with {} {} at {} ({}) on {}'.format(self.attributes['size'],
                                                                   self.attributes['currency'],
                                                                   self.attributes['open_price'],
                                                                   self.open_cost_basis,
                                                                   now)
        # print(ret)
        self.is_open = True

    def close(self, current_price, current_time):
        # sell self.size of self.currency
        # TODO: INTEGRATE API... ASAP!

        self.attributes.update({
            'close_price': float(current_price),
            'close_time': current_time,
        })
        try:
            now = self.attributes['close_time'].strftime("%m/%d/%Y, %H:%M:%S")
        except AttributeError:
            now = self.attributes['close_time']
        self.close_cost_basis = self.attributes['size'] * self.attributes['close_price']

        ret = 'position closed with {} {} at {} ({}) on {}'.format(self.attributes['size'],
                                                                   self.attributes['currency'],
                                                                   self.attributes['close_price'],
                                                                   self.close_cost_basis,
                                                                   now)

        # print(ret, end=' ')
        self.returns = self.close_cost_basis - self.open_cost_basis
        ret2 = 'for a return of {}'.format(self.returns)
        # print(ret2)
        self.is_open = False

    def __init__(self):
        self.is_open = False
