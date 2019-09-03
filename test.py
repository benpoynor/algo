from algos.sma_algo import MovingAverageAlgo
from masterclasses import RiskModel, Account, BacktestModel
import settings
import unittest


def get_stats() -> dict:
    Account().__init__()
    RiskModel().__init__()
    algorithm = None
    #TESTS CURRENTLY BROKEN.
    #TODO: FIX TESTS
    backtest_model = BacktestModel(algorithm=algorithm)

    gd = backtest_model.gen_backtest(settings.BACKTEST_CURRENCIES)
    return backtest_model.calc_backtest(gd).backtest_stats


class TestConstancy(unittest.TestCase):
    def test_stats(self):
        # this seems like a no-brainer, but could be failed
        # with an improper threading implementation
        self.assertEqual(get_stats(), get_stats())


class TestValues(unittest.TestCase):
    def test_sharpe(self):
        sharpe = float(get_stats().get('sharpe'))
        self.assertTrue(-5 < sharpe < 5)


if __name__ == '__main__':
    unittest.main()
