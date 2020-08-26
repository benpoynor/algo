
# basically all constants will be defined in this settings.py file

MKT_DATA_BASICS = ['open', 'low', 'close', 'high', 'volume']
# BACKTEST_CURRENCIES = ['ETH-USD', 'BTC-USD', 'LTC-USD', 'ZEC-USD']

BACKTEST_CURRENCIES = ['BTC-USD', 'ETH-USD', 'ZEC-USD', 'LTC-USD']

PERIODS = ['weekly', 'daily', '1min']
DATA_PATH = '/home/benjamin/dev/algo/data/'
BATCH_TEST_MODE = False
MINUTE_PERIODS_PER_YEAR = 525600
DAILY_PERIODS_PER_YEAR = 365
WEEKLY_PERIODS_PER_YEAR = 52
RISK_FREE_RATE = .0181  # U.S. Two Year Yield
STARTING_CAPITAL = 5000
FEE_SCHEDULE = .0035

CURRENT_PERIOD_SETTING = PERIODS[1]
CPY = DAILY_PERIODS_PER_YEAR
LONG_SMA_PERIOD = 15
SHORT_SMA_PERIOD = 7

DEBUG = False
