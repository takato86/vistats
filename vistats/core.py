import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple
from matplotlib import cbook


def boxplot_annotate_brackets(
    tuples: List[Tuple[int, int, str]], x: np.ndarray,
    dh=.05, barh=.05, text_dh=0.01, fs=None, ax=None,
    **boxplotkwargs
    ):
    """Annotate boxplot

    Args:
        tuples (List[Tuple[int, int, str]]): list of tuples including (idx1, idx2, text)
            :param idx1: number of left bar to put bracket over
            :param idx2: number of right bar to put bracket over
            :param text: string to write or number for generating asterixes
        x (np.ndarray): Data that will be represented in the boxplots. Should have 2 or fewer dimensions.
        dh (float, optional): height offset over bar / bar + yerr in axes coordinates (0 to 1). Defaults to .05.
        barh (float, optional): bar height in axes coordinates (0 to 1). Defaults to .05.
        text_dh (float, optional): _description_. Defaults to 0.01.
        fs (_type_, optional): how a text is over the line in axes cordinates(0 to 1). Defaults to None.
        ax (_type_, optional): font size. Defaults to None.
    """
    stats = cbook.boxplot_stats(x, **boxplotkwargs)
    height = [stat['q3'] for stat in stats]
    yerr = [stat['whishi'] - stat['q3'] for stat in stats]
    bars = np.arange(1, x.shape[1] + 1)
    annotate_brackets(
        tuples, bars, height, yerr, dh=dh, barh=barh, text_dh=text_dh, fs=fs, ax=ax
    )


def annotate_brackets(tuples: List[Tuple[int, int, str]], center: np.ndarray, 
                      height: np.ndarray, yerr: np.ndarray=None, dh=.05, 
                      barh=.05, text_dh=0.01, fs=None, ax=None):
    """ 
    Annotate plot with brackets and texts.
  
    :param tuples: list of tuples including (idx1, idx2, text)
        :param idx1: number of left bar to put bracket over
        :param idx2: number of right bar to put bracket over
        :param text: string to write or number for generating asterixes
    :param center: centers of all bars (like plt.bar() input)
    :param height: heights of all bars (like plt.bar() input)
    :param yerr: yerrs of all bars (like plt.bar() input)
    :param dh: height offset over bar / bar + yerr in axes coordinates (0 to 1)
    :param barh: bar height in axes coordinates (0 to 1)
    :param text_dh: how a text is over the line in axes cordinates(0 to 1)
    :param fs: font size (pt)
    """

    ax = ax if ax is not None else plt
    
    # sorting tuples by the first element of each tuple.
    sorted_values = [idx1 for idx1, _, _ in tuples]
    sorted_tuple_idxes = np.argsort(sorted_values)
    counter_idx = {i: 0 for i in range(len(center))}
    max_y = 0
    # get font size.
    fs = fs if fs is not None else plt.rcParams["font.size"]
    # pt to inch (1pt = 1/72 inch)
    fsinch = fs / 72
    # inch to pixel
    fspx = fsinch * plt.rcParams["figure.dpi"]

    # decide a margin over bar+yerr, a height of bar, a margin of text.
    origin_ax_min_y, origin_ax_max_y = plt.gca().get_ylim()
    fixed_dh = dh * (origin_ax_max_y - origin_ax_min_y)
    fixed_barh = barh * (origin_ax_max_y - origin_ax_min_y)
    fixed_text_dh = text_dh * (origin_ax_max_y - origin_ax_min_y)

    # estimate height
    # Note that the current axes will make large as the following process adds bars
    # These commands estimate the maximum y of the y-axis.
    p_miny, p_maxy = plt.gca().get_window_extent().get_points()[:, 1]
    # transform 1 dot per pixel
    font_height =  (origin_ax_max_y - origin_ax_min_y) * fspx / (p_maxy - p_miny)

    # Repeating 5 times empirically makes the loss less than 1.
    for _ in range(5):
        ax_max_y = origin_ax_max_y + fixed_dh + len(tuples) * (fixed_text_dh*2 + fixed_barh + font_height)
        # ajust font height
        # Get fontsize in the axes coordinates.
        font_height = fspx * (ax_max_y - origin_ax_min_y) / (p_maxy - p_miny)

    # plot brackets and texts.
    for tuple_idx  in sorted_tuple_idxes:
        idx1, idx2, text = tuples[tuple_idx]

        lx, ly = center[idx1], height[idx1] 
        rx, ry = center[idx2], height[idx2] 

        if yerr:
            ly += yerr[idx1]
            ry += yerr[idx2]
    
        base_y = max(ly, ry) + fixed_dh
        # bar + yerr / max_y plus the text with its margins.
        y = max(base_y, max_y + fixed_barh + fixed_text_dh + font_height + fixed_text_dh)

        if max_y < y:
            max_y = y
    
        barx = [lx, lx, rx, rx]
        bary = [y, y+fixed_barh, y+fixed_barh, y]
        mid = ((lx+rx)/2, y + fixed_barh + fixed_text_dh)
    
        ax.plot(barx, bary, c='black')
    
        kwargs = dict(ha='center', va='bottom')
        if fs is not None:
            kwargs['fontsize'] = fs
    
        kwargs['color'] = "black"
        ax.text(*mid, text, **kwargs)
        
        counter_idx[idx1] += 1
        counter_idx[idx2] += 1

