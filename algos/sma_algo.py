from masterclasses import Algorithm
from utilities.technicals import Technicals


class MovingAverageAlgo(Algorithm):
    def __init__(self):
        super().__init__()

    # TODO: add runtime type param that alters the action if backtesting or on live etc..
    # need a seperate action for backtesting and a seperate action for live testing and a seperate action for real life
    # or take in a runtime type paramater that 'backtesting' 'live testing' 'live'
    def action(self, index, data):
        if Technicals.sma(20, data, index) < Technicals.sma(50, data, index):
            if not self.position.is_open:
                self.position.open(1, 'BTC-USD', data[index].get('close'), data[index].get('formatted_date'))
        elif Technicals.sma(20, data, index) > Technicals.sma(50, data, index):
            if self.position.is_open:
                self.position.close(data[index].get('close'), data[index].get('formatted_date'))

        self.update_alpha()
