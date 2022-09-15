import seaborn as sns
import matplotlib.pyplot as plt


def polish(fig, ax, handle_zero_zero=True):
    """
    This is entirely copy and pasted from here
    https://github.com/Timothysit/sciplotlib/blob/master/module/polish.py

    Change the limit of axis spines so that they match the first and last tick marks
    Parameters
    -----------
    fig:
    ax:
    handle_zero_zero : bool
        whether to join axis if both have minimum take mark value of zero
        useful for creating unity plots / plots where (0, 0) has a special meaning.
    :return:
    """

    xmin, xmax = ax.get_xlim()
    all_xtick_loc = ax.get_xticks()
    visible_xtick = [t for t in all_xtick_loc if (t >= xmin) & (t <= xmax)]
    min_visible_xtick_loc = min(visible_xtick)
    max_visible_xtick_loc = max(visible_xtick)
    ax.spines['bottom'].set_bounds(min_visible_xtick_loc, max_visible_xtick_loc)

    ymin, ymax = ax.get_ylim()
    all_ytick_loc = ax.get_yticks()
    visible_ytick = [t for t in all_ytick_loc if (t >= ymin) & (t <= ymax)]
    min_visible_ytick_loc = min(visible_ytick)
    max_visible_ytick_loc = max(visible_ytick)
    ax.spines['left'].set_bounds(min_visible_ytick_loc, max_visible_ytick_loc)

    if handle_zero_zero:
        if min_visible_xtick_loc == 0 and min_visible_ytick_loc == 0:
            ax.set_xlim([0, xmax])
            ax.set_ylim([0, ymax])
    sns.despine(fig, ax)
    plt.tight_layout()
    return fig, ax
