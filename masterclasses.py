
class Algorithm:
    alpha: float

    def __init__(self):
        self.position = Position()
        self.alpha = 0.00

    def update_alpha(self):
        self.alpha += self.position.alpha

    def action(self, index, data):
        raise NotImplementedError


class Backtest:
    alpha: int
    beta: int
    delta: int
    sharpe: int

    def __init__(self, data, algorithm):
        for i in range(len(data)):
            algorithm.action(i, data)
        if algorithm.position.is_open:
            algorithm.alpha -= algorithm.position.open_cost_basis
        ret = 'alpha: {}'.format(algorithm.alpha)
        print(ret)


class Position:
    attributes = {}
    is_open: bool
    alpha = 0
    open_cost_basis: float
    close_cost_basis: float

    def open(self, order_size,
             currency, current_price,
             current_time):
        # later i need to add open_limit, open_market, open_large, open_small, etc...
        # for now though, this is OK, no reason to abstract so far into future yet...
        self.alpha = 0
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
        print(ret)
        self.is_open = True

    def close(self, current_price, current_time):
        # sell self.size of self.currency

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

        print(ret, end=' ')
        self.alpha = self.close_cost_basis - self.open_cost_basis
        ret2 = 'for a return of {}'.format(self.alpha)
        print(ret2)
        self.is_open = False

    def __init__(self):
        self.is_open = False
