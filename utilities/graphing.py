import pandas as pd
import matplotlib.pyplot as plt
from mpl_finance import candlestick2_ochl
from utilities.technicals import Technicals
import numpy as np


def add_titlebox(ax, text):
    ax.text(.55, .8, text,
            horizontalalignment='center',
            transform=ax.transAxes,
            bbox=dict(facecolor='white', alpha=0.6),
            fontsize=12.5)
    return ax


def moving_average_full_graph(data, short_period, long_period, hist_array):
    # setup window
    plt.subplots_adjust(left=.03, bottom=.03, right=0.99, top=0.99, wspace=0.05, hspace=0.15)
    dataset = pd.DataFrame(data=data)
    x = np.arange(len(dataset))
    gridsize = (8, 2)

    # declare axes
    ax1 = plt.subplot2grid(gridsize, (0, 0), colspan=2, rowspan=4)
    ax2 = plt.subplot2grid(gridsize, (4, 0), colspan=2, rowspan=1, sharex=ax1)
    ax3 = plt.subplot2grid(gridsize, (5, 0), colspan=2, rowspan=1, sharex=ax1)
    ax4 = plt.subplot2grid(gridsize, (6, 0), colspan=2, rowspan=1, sharex=ax1)
    ax5 = plt.subplot2grid(gridsize, (7, 0), colspan=2, rowspan=1, sharex=ax1)

    sma_short = Technicals.pandas_sma(short_period, dataset)
    sma_long = Technicals.pandas_sma(long_period, dataset)
    dydxshort = Technicals.calc_derivative(sma_short)
    dydxlong = Technicals.calc_derivative(sma_long)
    sma_delta = sma_short - sma_long
    sma_delta_dydx = Technicals.calc_derivative(sma_delta)
    sma_delta_dydx2 = Technicals.calc_derivative(sma_delta_dydx)

    # first box
    candlestick2_ochl(ax=ax1, opens=dataset['open'], closes=dataset['close'],
                      highs=dataset['high'], lows=dataset['low'],
                      width=1, alpha=1, colorup='green', colordown='red', )

    sma_short.plot(ax=ax1, color='blue')
    sma_long.plot(ax=ax1, color='red')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Price')

    for i in hist_array:
        if i.get('open_index'):
            ax1.plot(i.get('open_index'), i.get('open_price'), '^', color='black', markersize=10)
        if i.get('close_index'):
            ax1.plot(i.get('close_index'), i.get('close_price'), 'v', color='black', markersize=10)

    # second box
    dydxshort.plot(ax=ax2, color='blue')
    dydxlong.plot(ax=ax2, color='red')
    ax2.set_ylabel('Dy/Dx of SMA(s)')

    # third box
    sma_delta.plot(ax=ax3, color='purple')
    ax3.set_ylabel('SMA delta')
    ax3.fill_between(x, sma_delta, 0, where=sma_delta >= 0, facecolor='green', interpolate=True, alpha=.5)
    ax3.fill_between(x, sma_delta, 0, where=sma_delta <= 0, facecolor='red', interpolate=True, alpha=.5)

    # fourth box
    sma_delta_dydx.plot(ax=ax4)
    ax4.set_ylabel('Dy/Dx of SMA(s)')

    # fifth box
    sma_delta_dydx2.plot(ax=ax5)
    ax5.set_ylabel('Dy/Dx of SMA Delta')
    ax5.set_xlabel('date')

    dx_axs = [ax2, ax3, ax4, ax5]
    for a in dx_axs:
        a.axhline(0, linestyle='dashed', color='xkcd:dark grey',
                  alpha=0.6, label='Full-period mean', marker='')

    mng = plt.get_current_fig_manager()
    mng.resize(*mng.window.maxsize())
    plt.show()
