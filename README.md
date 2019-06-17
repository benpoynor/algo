Algorithmic Cryptocurrency Trading
========
### Structure and Design Philosophy:
main controller  
V  
backtest/live instantiates algorithm  
V  
backtest/live loops through algorithm action  
V  
algorithm action actually happens  
V  
opens and closes positions based on logic  
V  
positions interact with API

#### futures plans
- multithreading algorithm instances, multiple live algos trading at once
- website where I can monitor trades and trade history
- running on AWS near binance exchange servers

#### deps:
mpl_finance
https://github.com/matplotlib/mpl_finance

yahoofinancials
https://github.com/JECSand/yahoofinancials

#### Api stuff:
binance API docs:
https://github.com/binance-exchange/binance-official-api-docs
