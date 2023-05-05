import os
from typing import List

from stats import Stats


def is_pdf_file(name: str):
    if os.path.splitext(name)[1].lower() == '.pdf':
        return True
    return False


# stats helpers
def print_stats(stats: List[Stats]):
    for stat in stats:
        print(stat)


def save_stat_total_size(size: int, stats: List[Stats]):
    stats.append(Stats('Total size', size, 'bytes'))


def save_stat_pdf_total_size(size: int, stats: List[Stats]):
    stats.append(Stats('Total PDF size', size, 'bytes'))
