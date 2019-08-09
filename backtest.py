from algos.sma_algo import MovingAverageAlgo
from masterclasses import RiskModel, ExecutionModel, Account, BacktestModel
from settings import BACKTEST_CURRENCIES as BC
import argparse


def main(**kwargs):
    Account(), RiskModel(), ExecutionModel()
    algorithm = MovingAverageAlgo(bc=BC)
    backtest_model = BacktestModel(algorithm=algorithm)
    if not kwargs.get('no_gui'):
        backtest_model.visualize_backtest(BC[0])
    else:
        backtest_model.print_backtest()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run Backtest')
    parser.add_argument("--no-gui", type=bool, nargs='?',
                        const=True, default=False,
                        help="Deactivate matplot graph")

    namespace = vars(parser.parse_args())
    main(**namespace)
