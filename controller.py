from algos.sma_algo import MovingAverageAlgo
from masterclasses import RiskModel, ExecutionModel, Account, BacktestModel
from settings import BACKTEST_CURRENCIES as BC

if __name__ == "__main__":
    account = Account()
    risk_model = RiskModel(account)
    execution_model = ExecutionModel(account)
    algorithm = MovingAverageAlgo(execution_model, risk_model)
    backtest_model = BacktestModel(algorithm, account)

    backtest_model.backtest('BTC-USD')
