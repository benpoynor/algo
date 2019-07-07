from algos.sma_algo import MovingAverageAlgo
from masterclasses import RiskModel, ExecutionModel, Account, BacktestModel
from settings import BACKTEST_CURRENCIES as BC
from pprint import pprint


if __name__ == "__main__":
    account = Account()
    risk_model = RiskModel()
    execution_model = ExecutionModel()
    algorithm = MovingAverageAlgo()
    backtest_model = BacktestModel(algorithm=algorithm)

    backtest_model.visualize_backtest('ETH-USD')
