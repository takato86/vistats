import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple


def barplot_annotate_brackets(tuples: List[Tuple[int, int, str]], center: np.ndarray, 
                              height: np.ndarray, yerr: np.ndarray=None, dh=.05, 
                              barh=.05, text_dh=0.02, fs=None):
    """ 
    Annotate barplot with p-values.
  
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
    :param fs: font size
    """
    
    # sorting tuples by the first element of each tuple.
    sorted_values = [idx1 for idx1, _, _ in tuples]
    sorted_tuple_idxes = np.argsort(sorted_values)
    counter_idx = {i: 0 for i in range(len(center))}
    max_y = 0
    # get font size.
    fs = fs if fs is not None else plt.rcParams["font.size"]

    # decide a margin over bar+yerr, a height of bar, a margin of text.
    ax_min_y, ax_max_y = plt.gca().get_ylim()
    fixed_dh = dh * (ax_max_y - ax_min_y)
    fixed_barh = barh * (ax_max_y - ax_min_y)
    fixed_text_dh = text_dh * (ax_max_y - ax_min_y)

    # estimate height
    # Note that the current axes will make large as the following process adds bars
    # These commands estimate the maximum y of the y-axis.
    p_miny, p_maxy = plt.gca().get_window_extent().get_points()[:, 1]
    font_height = fs * (ax_max_y - ax_min_y) / (p_maxy - p_miny)
    ax_max_y += fixed_dh + len(tuples) * (fixed_text_dh*2 + fixed_barh + font_height)

    # ajust font height
    # Get fontsize in the axes coordinates.
    font_height = fs * (ax_max_y - ax_min_y) / (p_maxy - p_miny)

    for tuple_idx  in sorted_tuple_idxes:
        idx1, idx2, text = tuples[tuple_idx]

        lx, ly = center[idx1], height[idx1] 
        rx, ry = center[idx2], height[idx2] 

        if yerr:
            ly += yerr[idx1]
            ry += yerr[idx2]
    
        y = max(ly, ry) + fixed_dh
        # bar + yerr / max_y plus the text with its margins.
        y = max(y, max_y + fixed_barh + 2*fixed_text_dh + font_height*1.5)

        if max_y < y:
            max_y = y
    
        barx = [lx, lx, rx, rx]
        bary = [y, y+fixed_barh, y+fixed_barh, y]
        mid = ((lx+rx)/2, y + font_height / 2 + fixed_text_dh)
    
        plt.plot(barx, bary, c='black')
    
        kwargs = dict(ha='center', va='bottom')
        if fs is not None:
            kwargs['fontsize'] = fs
    
        kwargs['color'] = "black"
        plt.text(*mid, text, **kwargs)
        
        counter_idx[idx1] += 1
        counter_idx[idx2] += 1

