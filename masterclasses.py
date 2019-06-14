from datetime import datetime


class Algorithm:
    positions = []
    stop_loss: float  # -.02 (-2%)
    alpha: int

    def __init__(self):
        alpha = 0
        print("Algorithm Superclass Instantiated...")

    def liquidate(self):
        for position in self.positions:
            position.close()

    def update_alpha(self):
        for position in self.positions:
            self.alpha += position.alpha

    def action(self, current, data):
        raise NotImplementedError


class Backtest:
    alpha: int
    beta: int
    delta: int
    sharpe: int

    def __init__(self, data, algorithm):
        for point in data:
            algorithm.action(current=point, data=data)

        algorithm.update_alpha()
        print('alpha: {}').format(algorithm.alpha)


class Position:
    exposure: str  # 'long', 'short'
    currency: str  # 'BTC', 'ETH'
    size: int
    is_open: bool

    open_time: datetime
    close_time: datetime

    open_price: int
    close_price: int
    current_price: int

    alpha: int

    def open(self):
        # buy self.size of self.currency if long
        # sell self.size of self.currency if short
        self.open_time = datetime.now()
        self.is_open = True
        pass

    def close(self):
        # sell self.size of self.currency if long
        # buy self.size of self.currency if short
        self.close_time = datetime.now()
        self.is_open = False
        pass

    def __init__(self, exposure, currency, size):
        self.exposure = exposure
        self.currency = currency
        self.size = size

        self.open()
