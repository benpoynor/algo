from algos.sma_algo import MovingAverageAlgo
from masterclasses import BacktestController
from settings import BACKTEST_CURRENCIES as BC


def run_all_backtests():
    a = MovingAverageAlgo()
    b = BacktestController(BC, a)
    b.full_backest(verbose=True)


if __name__ == "__main__":
    run_all_backtests()
