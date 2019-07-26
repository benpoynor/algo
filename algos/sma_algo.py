from masterclasses import Algorithm


class MovingAverageAlgo(Algorithm):
    def __init__(self, bc):
        self.positions = {}
        for c in bc:
            self.positions.update({c: False})

    def backtest_action(self, short_sma, long_sma, currency):
        if short_sma > long_sma:
            if not self.positions.get(currency):
                # price = float(data[index].get('close'))
                # self.execution_model.backtest_buy(price, index)
                self.positions.update({currency: True})
                return {'action': 'buy',
                        'signal_str': 1,
                        'liquidate': False}
            else:
                return {'action': 'pass',
                        'signal_str': 1,
                        'liquidate': False}

        elif short_sma < long_sma:
            if self.positions.get(currency):
                # price = float(data[index].get('close'))
                # self.execution_model.backtest_sell(price, index)
                self.positions.update({currency: False})
                return {'action': 'sell',
                        'signal_str': 1,
                        'liquidate': False}
            else:
                return {'action': 'pass',
                        'signal_str': 1,
                        'liquidate': False}
        else:
            return {'action': 'pass',
                    'signal_str': 1,
                    'liquidate': False}

    def action(self):
        pass
