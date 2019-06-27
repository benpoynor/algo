Algorithmic Cryptocurrency Trading
========
## Structure and Design Philosophy:
  
#### account: 
* holds account details (balance, keys, etc...)  

#### risk model: 
* decides how much to buy (manages risk)  

#### execution model: 
* buys  
#### algorithm: 
* tells when to buy  
#### backtest: 
* shows what would happen if the algorithm ran  

#### live: 
* actually runs the algorithm in real time  

#### future plans
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
