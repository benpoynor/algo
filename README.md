ALGO:

How to run:
pip install -r requirements.txt
"python main.py -h" to show options
"python main.py backtest" to do a simple backtest


Old project, accrued too much technical debt to continue to scale and add features without hacky implementation.
Definitely salvagable with some time, and definitely a good reference for anyone looking to build backtesting software. Bear in mind that this is a model of what not to do as much as it is a model of what to do. I built this over a year ago in my free time and as my first attempt at writing trading software.

Essentially it runs through a set of price data with a set of instructions on when to buy and sell, trades as if it were real time, and reports the algorithm's statistics via matplotlib visualizations and plaintext statistics. 


Structure and Design Philosophy:

account: holds account details (balance, keys, etc...)  
risk model: decides how much to buy (manages risk)  
execution model: buys  
algorithm: tells when to buy  
backtest: shows what would happen if the algorithm ran  
live: actually runs the algorithm in real time  
