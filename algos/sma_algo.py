from masterclasses import Algorithm
from utilities import data as technicals
from datetime import datetime


class MovingAverageAlgo(Algorithm):
    def __init__(self):
        super().__init__()

    # need a seperate action for backtesting and a seperate action for live testing and a seperate action for real life
    # or take in a runtime type paramater that 'backtesting' 'live testing' 'live'
    def action(self, index, data):
        if technicals.sma(20, data, index) < technicals.sma(50, data, index):
            if not self.position.is_open:
                self.position.open(1, 'BTC-USD', data[index].get('close'), data[index].get('formatted_date'))
        elif technicals.sma(20, data, index) > technicals.sma(50, data, index):
            if self.position.is_open:
                self.position.close(data[index].get('close'), data[index].get('formatted_date'))

        self.update_alpha()
