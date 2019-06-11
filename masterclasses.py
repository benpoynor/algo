from datetime import datetime


class Algorithm:
    positions = []
    stop_loss = float  # -.02 (-2%)

    def __init__(self):
        print("Algorithm Superclass Instantiated...")

    def liquidate(self):
        for position in self.positions:
            position.close()

    def check_stop(self, position):
        if position.alpha < self.stop_loss:
            position.close()

    def action(self):
        raise NotImplementedError


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
