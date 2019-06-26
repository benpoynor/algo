from masterclasses import Algorithm, RiskModel, ExecutionModel
from utilities.technicals import Technicals


class MovingAverageAlgo(Algorithm):
    def __init__(self):
        super().__init__(ExecutionModel())
        self.position_open = False

    def backtest_action(self, index, data, currency):
        if Technicals.sma(20, data, index) < Technicals.sma(50, data, index):
            self.execution_model.backtest_buy(data[index].get('close'))

        elif Technicals.sma(20, data, index) > Technicals.sma(50, data, index):
            self.execution_model.backtest_sell()

    def action(self, index, data, currency):
        pass
