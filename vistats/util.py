from typing import Any, List, Tuple
from scipy.stats._result_classes import TukeyHSDResult


def pvalue2notion(pvalue: float) -> str:
    """ transform pvalue to statistical notion; *:p<.05, **:p<.01

    Args:
        pvalue (float): _description_

    Returns:
        str: _description_
    """
    notion = ''

    if pvalue < 0.05:
        notion += '*'
    if pvalue < 0.01:
        notion += '*'
    
    return notion


def tukeyhsd_result2asterisk_tuples(result: TukeyHSDResult) -> List[Tuple[int, int, str]]:
    
    asterisk_tuples: List[Tuple[int, int, str]] = []
    for i in range(len(result.pvalue)):
        for j in range(i, len(result.pvalue)):
            pvalue = result.pvalue[i, j]
            notion = pvalue2notion(pvalue)
            if len(notion) > 0:
                asterisk_tuples.append((i, j, pvalue2notion(pvalue)))

    return asterisk_tuples


def ttest_result2asterisk_tuples(result: Any) -> List[Tuple[int, int, str]]:

    return [(0, 1, pvalue2notion(result.pvalue))]
