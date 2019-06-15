from masterclasses import Algorithm
from utilities import data as technicals


class MovingAverageAlgo(Algorithm):
    def __init__(self):
        super().__init__()

    def action(self, current, data):
        if technicals.sma(20, data, current) > technicals.sma(50, data, current):
            self.buy()
        elif technicals.sma(20, data, current) > technicals.sma(50, data, current):
            if self.position.is_open:
                self.sell()

        self.update_alpha()
