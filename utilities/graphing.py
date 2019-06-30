import pandas as pd
import matplotlib.pyplot as plt
from mpl_finance import candlestick2_ochl
from utilities.technicals import Technicals


def add_titlebox(ax, text):
    ax.text(.55, .8, text,
            horizontalalignment='center',
            transform=ax.transAxes,
            bbox=dict(facecolor='white', alpha=0.6),
            fontsize=12.5)
    return ax


def full_graph(data):
    plt.subplots_adjust(left=.03, bottom=.03, right=0.99, top=0.99, wspace=0.05, hspace=0.15)
    dataset = pd.DataFrame(data=data)
    gridsize = (8, 2)
    ax1 = plt.subplot2grid(gridsize, (0, 0), colspan=2, rowspan=4)
    ax2 = plt.subplot2grid(gridsize, (4, 0), colspan=2, rowspan=1)
    ax3 = plt.subplot2grid(gridsize, (5, 0), colspan=2, rowspan=1)
    ax4 = plt.subplot2grid(gridsize, (6, 0), colspan=1, rowspan=2)
    ax5 = plt.subplot2grid(gridsize, (6, 1), colspan=1, rowspan=2)

    ax1.set_xlabel('Date')
    ax1.set_ylabel('Price')
    ax2.set_ylabel('Dy/Dx of SMA(s)')
    ax3.set_ylabel('D^2y/Dx^2 of SMA(s)')
    ax4.set_xlabel('Date')
    ax4.set_ylabel('SMA delta')
    ax5.set_xlabel('Date')
    ax5.set_ylabel('Dy/Dx of SMA Delta')

    candlestick2_ochl(ax=ax1, opens=dataset['open'], closes=dataset['close'],
                      highs=dataset['high'], lows=dataset['low'],
                      width=1, alpha=1, colorup='green', colordown='red',)

    sma_50 = Technicals.pandas_sma(50, dataset)
    sma_20 = Technicals.pandas_sma(20, dataset)
    dydx20 = Technicals.calc_derivative(sma_20)
    dydx50 = Technicals.calc_derivative(sma_50)
    dydx2_20 = Technicals.calc_derivative(dydx20)
    dydx2_50 = Technicals.calc_derivative(dydx50)
    sma_delta = sma_50 - sma_20
    sma_delta_dydx = Technicals.calc_derivative(sma_delta)

    dydx20.plot(ax=ax2)
    dydx50.plot(ax=ax2)
    dydx2_20.plot(ax=ax3)
    dydx2_50.plot(ax=ax3)
    sma_delta.plot(ax=ax4)
    sma_delta_dydx.plot(ax=ax5)
    dx_axs = [ax2, ax3, ax4, ax5]
    for a in dx_axs:
        a.axhline(0, linestyle='dashed', color='xkcd:dark grey',
                  alpha=0.6, label='Full-period mean', marker='')
    sma_50.plot(ax=ax1)
    sma_20.plot(ax=ax1)
    mng = plt.get_current_fig_manager()
    mng.resize(*mng.window.maxsize())

    plt.show()
