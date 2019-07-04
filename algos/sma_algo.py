from masterclasses import Algorithm


class MovingAverageAlgo(Algorithm):
    def __init__(self):
        self.position_open = False

    def backtest_action(self, short_sma, long_sma):
        if short_sma > long_sma:
            if not self.position_open:
                # price = float(data[index].get('close'))
                # self.execution_model.backtest_buy(price, index)
                self.position_open = True
                return {'action': 'buy',
                        'signal_str': 1}
            else:
                return {'action': 'pass',
                        'signal_str': 1}

        elif short_sma < long_sma:
            if self.position_open:
                # price = float(data[index].get('close'))
                # self.execution_model.backtest_sell(price, index)
                self.position_open = False
                return {'action': 'sell',
                        'signal_str': 1}
            else:
                return {'action': 'pass',
                        'signal_str': 1}
        else:
            return {'action': 'pass',
                    'signal_str': 1}

    def action(self):
        pass
