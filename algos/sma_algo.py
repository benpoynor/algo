from masterclasses import Algorithm
from utilities import data as technicals


class MovingAverageAlgo(Algorithm):
    def __init__(self):
        super().__init__()

    def action(self, index, data):
        if technicals.sma(20, data, index) > technicals.sma(50, data, index):
            if not self.position.is_open:
                self.buy()
        elif technicals.sma(20, data, index) < technicals.sma(50, data, index):
            if self.position.is_open:
                self.sell()

        self.update_alpha()
