import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from mpl_toolkits.axes_grid1 import make_axes_locatable


def error_bars(x: str, y: str, data: pd.DataFrame, central_tendency: str = 'median',
               error_method: str = 'percentile',
               sections: dict = None, colors: list = None,
               xlim: tuple = None, cax_percentage: str = "40%"):
    """
    Plot fancy error bar
    Design is basically copied from this recent Covid-19 paper: https://www.medrxiv.org/content/10.1101/2021.03.25.21254330v1.full.pdf

    :param x: name of dataframe column containing values to be plotted
    :param y: name of dataframe column containing bar groups
    :param data: pandas dataframe
    :param central_tendency: 'median' or 'mean'
    :param error_method: 'percentile' or 'standard_deviation'
    :param sections: dictionary of section names and corresponding group names
    :param colors: list of colors, length should correspond to number of sections or groups
    :param xlim: x axis limits
    :param cax_percentage: how big do you want the y labels to be
    :return:
        fig: matplotlib figure
        ax: matplotlib main plot axis
        cax: additional matplotlib axis for y tick label
    """
    n_sections = None
    y_coord_sections = None

    # get colors and y coords
    if sections:
        n_sections = len(sections.keys())

        if colors is None:
            colors = sns.color_palette('colorblind', n_sections)
        else:
            if len(colors) != n_sections:
                raise RuntimeError("Number of colors has to match number of sections.")

        colors_bars = list()
        y_coord_bars = list()
        y_coord_sections = list()
        y_coord = 0
        names = list()
        for section_i, section_bars in enumerate(sections.values()):
            y_coord_sections.append(y_coord)
            y_coord -= 0.25

            for bar_name in section_bars:
                names.append(bar_name)
                y_coord -= 0.5
                y_coord_bars.append(y_coord)
                y_coord -= 0.5
                colors_bars.append(colors[section_i])
            y_coord -= 0.25
        n_bars = len(names)
    else:
        names = data[y].unique()
        n_bars = len(names)
        y_coord = 0
        y_coord_bars = list()
        for bar_name in names:
            y_coord -= 0.5
            y_coord_bars.append(y_coord)
            y_coord -= 0.5

        if colors is None:
            colors_bars = sns.color_palette('colorblind', n_bars)
        else:
            if len(colors) != n_bars:
                raise RuntimeError("Number of colors has to match number of groups in data.")
            colors_bars = colors

    # compute central tendency
    if central_tendency == 'median':
        ct_method = np.median
    elif central_tendency == 'mean':
        ct_method = np.mean
    else:
        raise NotImplementedError("central_tendency has to be either 'mean' or 'median'.")
    m = np.zeros(n_bars)
    for i, b in enumerate(names):
        m[i] = ct_method(data.loc[data[y] == b, x].values)

    # compute error bars
    if error_method == 'percentile':
        li, lq, ui, uq = np.zeros(n_bars), np.zeros(n_bars), np.zeros(n_bars), np.zeros(n_bars)
        for i, b in enumerate(names):
            li[i], lq[i], uq[i], ui[i] = np.percentile(data.loc[data[y] == b, x].values,
                                                       [2.5, 25, 75, 97.5])
    elif error_method == 'standard_deviation':
        sd = np.zeros(n_bars)
        for i, b in enumerate(names):
            sd[i] = np.std(data.loc[data[y] == b, x].values)
        li, lq = None, m - sd
        ui, uq = None, m + sd
    elif error_method == 'confidence_interval':
        raise NotImplementedError("error_method 'confidence_interval' is not yet supported.")
    elif error_method == 'None':
        li, lq = None, m
        ui, uq = None, m
    else:
        raise NotImplementedError("error_method {} is not supported.".format(error_method))

    # start drawing the figure
    # todo: check if we really need GridSpec here
    fig = plt.figure(constrained_layout=True, figsize=(5, 4), dpi=400)
    gs = gridspec.GridSpec(ncols=3, nrows=4, figure=fig)
    ax = fig.add_subplot(gs[:, :])

    # plot error bars
    for bar_i in range(n_bars):
        y_coord = y_coord_bars[bar_i]
        if li:
            ax.plot([li[bar_i], ui[bar_i]], [y_coord, y_coord], color=colors_bars[bar_i], alpha=0.35, linewidth=1,
                    solid_capstyle='round')
        ax.plot([lq[bar_i], uq[bar_i]], [y_coord, y_coord], color=colors_bars[bar_i], alpha=0.85, linewidth=1,
                solid_capstyle='round')

    if xlim is None:
        xmin, xmax = ax.get_xlim()
    else:
        xmin, xmax = xlim

    # plot grey shadow for bars
    for bar_i in range(n_bars):
        start = y_coord_bars[bar_i] + 0.48
        end = y_coord_bars[bar_i] - 0.48
        ax.fill_between(
            [xmin, xmax],
            [end, end],
            [start, start],
            color='#939596', alpha=0.15, linewidth=0)

    # plot grey shadow for section dividers
    if sections:
        for section_i in range(n_sections):
            start = y_coord_sections[section_i] + 0.23
            end = y_coord_sections[section_i] - 0.23
            ax.fill_between(
                [xmin, xmax],
                [end, end],
                [start, start],
                color='#939596', alpha=0.25, linewidth=0)

    # plot scatter points for central tendency
    ax.scatter(m, y_coord_bars, marker="o", color=colors_bars, s=6, edgecolors=colors_bars, facecolor="white",
               zorder=5)

    # style
    y_min = y_coord_bars[-1] - 0.5
    ax.set_ylim([y_min, 0.25])
    ax.set_xlim([xmin, xmax])
    ax.spines['bottom'].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.yaxis.set_ticks_position('none')
    ax.xaxis.set_ticks_position('none')

    # plot additional axis to get fancy y tick labels
    divider = make_axes_locatable(ax)
    # 50% might be adjusted depending on the length of the y tick labels
    cax = divider.append_axes("left", size=cax_percentage, pad=0)

    cax.get_xaxis().set_visible(False)
    cax.get_yaxis().set_visible(False)
    cax.spines['bottom'].set_visible(False)
    cax.spines["right"].set_visible(False)
    cax.spines["left"].set_visible(False)
    cax.spines["top"].set_visible(False)
    cax.set_ylim([y_min, 0.25])
    cax.set_xlim([xmin, xmax])

    # plot grey shadow for bars
    for bar_i in range(n_bars):
        start = y_coord_bars[bar_i] + 0.48
        end = y_coord_bars[bar_i] - 0.48
        cax.fill_between(
            [xmin, xmax],
            [end, end],
            [start, start],
            color=colors_bars[bar_i], alpha=0.15, linewidth=0)
        cax.text(xmax - 0.05 * (xmax - xmin), y_coord_bars[bar_i], names[bar_i],
                 verticalalignment='center', horizontalalignment='right',
                 fontsize=7)

    # plot grey shadow for section dividers
    if sections:
        section_names = list(sections.keys())
        for section_i in range(n_sections):
            start = y_coord_sections[section_i] + 0.23
            end = y_coord_sections[section_i] - 0.23
            cax.fill_between(
                [xmin, xmax],
                [end, end],
                [start, start],
                color=colors[section_i], alpha=0.25, linewidth=0)
            cax.text(xmax - 0.05 * (xmax - xmin), y_coord_sections[section_i], section_names[section_i],
                     verticalalignment='center', horizontalalignment='right',
                     fontsize=5)

    return fig, ax, cax


if __name__ == "__main__":
    tips = sns.load_dataset("tips")

    sections = {'Working Days': ['Thur', 'Fri'],
                'Weekend': ['Sat', 'Sun']}

    error_bars(x='total_bill', y='day', sections=sections,
               data=tips, error_method='percentile')
    plt.savefig('total_bills_per_day_sections.png')
    plt.show()

    error_bars(x='total_bill', y='day',
               data=tips, error_method='percentile')
    plt.savefig('total_bills_per_day.png')
    plt.show()

    error_bars(x='tip', y='time', data=tips, error_method='percentile')
    plt.savefig('total_tips_per_time.pdf')
    plt.show()
