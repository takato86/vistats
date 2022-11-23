import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple


def barplot_annotate_brackets(tuples: List[Tuple[int, int, str]], center: np.ndarray, 
                              height: np.ndarray, yerr: np.ndarray=None, dh=.05, 
                              barh=.05, fs=None, offset_basis=0.9):
    """ 
    Annotate barplot with p-values.
  
    :param tuples: list of tuples including (idx1, idx2, data)
    :param idx1: number of left bar to put bracket over
    :param idx2: number of right bar to put bracket over
    :param data: string to write or number for generating asterixes
    :param center: centers of all bars (like plt.bar() input)
    :param height: heights of all bars (like plt.bar() input)
    :param yerr: yerrs of all bars (like plt.bar() input)
    :param dh: height offset over bar / bar + yerr in axes coordinates (0 to 1)
    :param barh: bar height in axes coordinates (0 to 1)
    :param fs: font size
    """
    
    # 最小のindexを決める。
    ucb = center + yerr
    sorted_values = [idx1 for idx1, idx2, text in tuples]
    sorted_tuple_idxes = np.argsort(sorted_values)
    counter_idx = {i: 0 for i in range(len(center))}
    max_y = 0

    for tuple_idx  in sorted_tuple_idxes:
        idx1, idx2, text = tuples[tuple_idx]

        offset_ly = counter_idx[idx1] * offset_basis
        offset_ry = counter_idx[idx2] * offset_basis

        # 中心、高さの指定
        lx, ly = center[idx1], height[idx1] + offset_ly
        rx, ry = center[idx2], height[idx2] + offset_ry

        if yerr:
            ly += yerr[idx1]
            ry += yerr[idx2]
    
        ax_y0, ax_y1 = plt.gca().get_ylim()
        fixed_dh = dh * (ax_y1 - ax_y0)
        fixed_barh = barh * (ax_y1 - ax_y0)
    
        y = max(ly, ry) + fixed_dh
        # max_yより高い位置
        y = max(y, max_y + fixed_dh + fixed_barh)

        if max_y < y:
            max_y = y
    
        barx = [lx, lx, rx, rx]
        bary = [y, y+fixed_barh, y+fixed_barh, y]
        mid = ((lx+rx)/2, y+fixed_barh)
    
        plt.plot(barx, bary, c='black')
    
        kwargs = dict(ha='center', va='bottom')
        if fs is not None:
            kwargs['fontsize'] = fs
    
        kwargs['color'] = "black"
        plt.text(*mid, text, **kwargs)
        
        counter_idx[idx1] += 1
        counter_idx[idx2] += 1

