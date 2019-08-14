from algos.sma_algo import MovingAverageAlgo
from masterclasses import RiskModel, ExecutionModel, Account, BacktestModel
from settings import BACKTEST_CURRENCIES as BC
import argparse
import os


def main(**kwargs):
    def backtest():
        currencies = BC
        if kwargs.get('sc'):
            print('isolating: {}'.format(kwargs.get('sc')))
            currencies = currencies.pop(currencies.index(kwargs.get('sc')[0]))

        Account(), RiskModel(), ExecutionModel()
        algorithm = MovingAverageAlgo(bc=currencies)
        backtest_model = BacktestModel(algorithm=algorithm)

        if not kwargs.get('no_gui'):
            backtest_model.visualize_backtest(currencies[0])
        else:
            backtest_model.print_backtest()

    def test():
        print('running tests...')
        os.system('python -m unittest discover')

    def livedemo():
        print('not implemented yet')

    def production():
        print('not implemented yet')

    eval(kwargs['runtime'][0] + '()')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run main.py')
    parser.add_argument("--no-gui", type=bool, nargs='?',
                        const=True, default=False,
                        help="Deactivate matplot graph")
    parser.add_argument("-sc", type=str, nargs=1,
                        required=False, help="isolate one currency for backtest")

    parser.add_argument('runtime', metavar='T', type=str, nargs=1,
                        help='backtest, test, livedemo, production')
    namespace = vars(parser.parse_args())

    main(**namespace)
