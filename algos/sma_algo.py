from masterclasses import Algorithm, RiskModel
from utilities.technicals import Technicals


class MovingAverageAlgo(Algorithm):
    def __init__(self):
        super().__init__(RiskModel())
        self.position_open = False

    def backtest_action(self, index, data, currency):
        if Technicals.sma(20, data, index) < Technicals.sma(50, data, index):
            if not self.position_open:
                return 'buy'

        elif Technicals.sma(20, data, index) > Technicals.sma(50, data, index):
            if self.position_open:
                return 'sell'
        else:
            return 'pass'

    def action(self, index, data, currency):
        pass
