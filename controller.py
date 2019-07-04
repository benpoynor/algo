from algos.sma_algo import MovingAverageAlgo
from masterclasses import RiskModel, ExecutionModel, Account, BacktestModel
from settings import BACKTEST_CURRENCIES as BC
from pprint import pprint


if __name__ == "__main__":
    account = Account()
    risk_model = RiskModel(account)
    execution_model = ExecutionModel(account)
    algorithm = MovingAverageAlgo()
    backtest_model = BacktestModel(algorithm=algorithm,
                                   account=account,
                                   execution_model=execution_model,
                                   risk_model=risk_model)

    backtest_model.execute_backtest('ETH-USD')
