import pandas as pd
import matplotlib.pyplot as plt
from mpl_finance import candlestick2_ochl
from utilities.technicals import Technicals
import numpy as np
import settings


def add_titlebox(ax, text):
    ax.text(.55, .8, text,
            horizontalalignment='center',
            transform=ax.transAxes,
            bbox=dict(facecolor='white', alpha=0.6),
            fontsize=12.5)
    return ax


def populate_infobox(ax, display_dict, size=1):
    step = size / 30
    font = size * 15
    ax.text(.5, .95, 'Backtest Statistics',
            horizontalalignment='center',
            transform=ax.transAxes,
            bbox=dict(facecolor='white', alpha=0.6),
            fontsize=font * 2,
            family='monospace')
    for i, (k, v) in enumerate(display_dict.items()):
        ax.text(.1, .9 - (i * step), '{}: {}'.format(k, v),
                horizontalalignment='left',
                transform=ax.transAxes,
                bbox=dict(facecolor='white', alpha=0.6),
                fontsize=font,
                family='serif')


def moving_average_full_graph(default_currency: str, bs):

    data = bs.get_price_dataframe(default_currency)  # full set of price data
    short_period = settings.SHORT_SMA_PERIOD  # short period to plot a moving avg.
    long_period = settings.LONG_SMA_PERIOD  # ditto
    backtest_stats = bs.backtest_stats  # disgusting
    equity_history = bs.equity_history
    signal_data = bs.get_signal_list(default_currency)

    # setup window
    plt.subplots_adjust(left=.04, bottom=.03, right=0.99, top=0.99, wspace=0.05, hspace=0.15)
    dataset = pd.DataFrame(data=data)
    x_range = np.arange(len(dataset))
    gridsize = (8, 8)

    # declare axes
    ax1 = plt.subplot2grid(gridsize, (0, 0), colspan=6, rowspan=4)
    ax2 = plt.subplot2grid(gridsize, (4, 0), colspan=6, rowspan=1, sharex=ax1)
    ax3 = plt.subplot2grid(gridsize, (5, 0), colspan=6, rowspan=1, sharex=ax1)
    ax4 = plt.subplot2grid(gridsize, (6, 0), colspan=6, rowspan=1, sharex=ax1)
    ax5 = plt.subplot2grid(gridsize, (7, 0), colspan=6, rowspan=1, sharex=ax1)
    ax6 = plt.subplot2grid(gridsize, (0, 6), colspan=2, rowspan=8)

    sma_short = Technicals.pandas_sma(short_period, dataset)
    sma_long = Technicals.pandas_sma(long_period, dataset)
    dydxshort = Technicals.calc_derivative(sma_short)
    dydxlong = Technicals.calc_derivative(sma_long)
    sma_delta = sma_short - sma_long
    sma_delta_dydx = Technicals.calc_derivative(sma_delta)

    # first box
    candlestick2_ochl(ax=ax1, opens=dataset['open'], closes=dataset['close'],
                      highs=dataset['high'], lows=dataset['low'],
                      width=1, alpha=1, colorup='green', colordown='red', )

    sma_short.plot(ax=ax1, color='blue')
    sma_long.plot(ax=ax1, color='red')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Price', fontsize=20)

    for idx, val in enumerate(signal_data):
        if val.liquidate:
            ax1.plot(idx, float(dataset.at[idx, 'close']), 'X', color='red', markersize=10)
        elif val.action == 'buy':
            ax1.plot(idx, float(dataset.at[idx, 'close']), '^', color='black', markersize=10)
        elif val.action == 'sell':
            ax1.plot(idx, float(dataset.at[idx, 'close']), 'v', color='black', markersize=10)

    # second box
    dydxshort.plot(ax=ax2, color='blue')
    dydxlong.plot(ax=ax2, color='red')
    ax2.set_ylabel(r'$\frac{dy}{dx} \mu$', fontsize=20)

    # third box
    sma_delta.plot(ax=ax3, color='purple')
    ax3.set_ylabel(r'$\mu \Delta$', fontsize=20)
    ax3.fill_between(x_range, sma_delta, 0, where=sma_delta >= 0, facecolor='green', interpolate=True, alpha=.5)
    ax3.fill_between(x_range, sma_delta, 0, where=sma_delta <= 0, facecolor='red', interpolate=True, alpha=.5)

    # fourth box
    sma_delta_dydx.plot(ax=ax4)
    ax4.set_ylabel(r'$\frac{dy}{dx}(\mu \Delta$)', fontsize=20)

    # fifth box
    equity_history.plot(ax=ax5)
    ax5.set_ylabel(r'$equity$', fontsize=20)
    ax5.set_xlabel('date')
    gmax_idx = backtest_stats.get('gmax_idx')
    gmin_idx = backtest_stats.get('gmin_idx')

    if gmax_idx and gmin_idx:
        ax5.fill_between([gmax_idx, gmin_idx],
                         float(equity_history.at[gmin_idx, 0]),
                         float(equity_history.at[gmax_idx, 0]),
                         facecolor='red',
                         alpha=.25)

    # sixth box
    populate_infobox(ax6, backtest_stats)

    # draw line at 0 on the derivative graphs
    dx_axs = [ax2, ax3, ax4]
    for a in dx_axs:
        a.axhline(0, linestyle='dashed', color='xkcd:dark grey',
                  alpha=0.6, label='Full-period mean', marker='')

    mng = plt.get_current_fig_manager()
    mng.resize(*mng.window.maxsize())
    plt.show()


def debug_graph(equity_history):
    ax1 = plt.subplot2grid((1, 1), (0, 0))
    equity_history.plot(ax=ax1)
    mng = plt.get_current_fig_manager()
    mng.resize(*mng.window.maxsize())
    plt.show()
