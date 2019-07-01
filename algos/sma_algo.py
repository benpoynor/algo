from masterclasses import Algorithm
from utilities.technicals import Technicals


class MovingAverageAlgo(Algorithm):
    def __init__(self, execution_model, risk_model):
        self.execution_model = execution_model
        self.risk_model = risk_model
        self.position_open = False

    def backtest_action(self, index, data, hist_array):
        if Technicals.sma(20, data, index) < Technicals.sma(50, data, index):
            if not self.position_open:
                self.execution_model.backtest_buy(float(data[index].get('close')), index, hist_array)
                self.position_open = True

        elif Technicals.sma(20, data, index) > Technicals.sma(50, data, index):
            if self.position_open:
                self.execution_model.backtest_sell(float(data[index].get('close')), index, hist_array)
                self.position_open = False

    def action(self):
        pass
