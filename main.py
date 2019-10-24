from masterclasses import RiskModel, ExecutionModel, Account, BacktestModel
from settings import BACKTEST_CURRENCIES as BC
import argparse
import os

# TODO: ACTUALLY MAKE A GUI AT THE BEGINNING THAT THE BACKTEST IS RUN FROM!
# MAKES THIS SHIT LOOKS 1000X LESS FUCKING TERRIBLE THAN IT CURRENTLY DOES


def main(**kwargs):
    def backtest():

        # < eval(kwargs['runtime'][0] + '()') >
        # is run at the bottom, which is why it looks like backtest is never getting called
        # in actuality, the user-inputted string literal after main dictates...
        # the function that gets called here.
        # can it be written better? yes. Is it a priority? No.

        currencies = BC
        if kwargs.get('sc'):
            print('isolating: {}'.format(kwargs.get('sc')))
            currencies = currencies.pop(currencies.index(kwargs.get('sc')[0]))

        Account(), RiskModel(), ExecutionModel()
        backtest_model = BacktestModel()

        def get_kwarg(name: str) -> str:
            return kwargs.get(name)[0] if isinstance(kwargs.get(name), list) else kwargs.get(name)

        tf = get_kwarg('tf')
        points = get_kwarg('pts') if get_kwarg('pts') else 0

        if not kwargs.get('no_gui'):
            backtest_model.visualize_backtest(currencies[0], tf, points=points)
        else:
            backtest_model.print_backtest(tf, points=points)

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

    parser.add_argument('runtime', metavar='Runtime', type=str, nargs=1,
                        help='backtest, test, livedemo, production')

    parser.add_argument('-tf', type=str, nargs=1,
                        required=False, help='[\'weekly\', \'daily\', \'1min\']', default='daily')

    parser.add_argument("-pts", type=int, nargs=1, required=False, default=0,
                        help="Integer amount of points to backtest"
                             " (trims from front of data for relevancy)")
    namespace = vars(parser.parse_args())

    main(**namespace)
