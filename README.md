ALGO: glorified matplotlib for making and exploring backtests of trading strategies

preview:
![demo image](https://github.com/benpoynor/algo/blob/master/demo.png?raw=true)

How to run:
1. pip install -r requirements.txt (fix any version errors by just installing the package without a version number)
2. download git LFS
3. cd into the data folder
4. run git lfs fetch and git lfs pull
5. open settings __init__.py and change my old absolute path to wherever the data folder is living on your system (sorry)

now that you have the default data, you can run the program

"python main.py -h" to show options
"python main.py backtest" to do a simple backtest on the default algo with the default datasets and settings


Old project, accrued too much technical debt to continue to scale and add features without hacky implementation.
Definitely salvagable with some time, and definitely a good reference for anyone looking to build backtesting software. Bear in mind that this is a model of what not to do as much as it is a model of what to do. I built this over a year ago in my free time and as my first attempt at writing trading software.

Essentially it runs through a set of price data with a set of instructions on when to buy and sell, trades as if it were real time, and reports the algorithm's statistics via matplotlib visualizations and plaintext statistics. 
