# coding:utf-8

import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict
from collections import Counter
from pandas import DataFrame, Series


path = 'data/usagov.txt'
records = [json.loads(i) for i in open(path)]


# 使用python标准库
def count_data(data):
    count = defaultdict(int)
    for key in data:
        count[key] = count[key] + 1

    return count


count_tz_dict = count_data([rz['tz'] for rz in records if 'tz' in rz])
print(count_tz_dict)


# 标准库排序 字典->Counter(dict).most(排名数) 获得数量倒序排列
def top_counts_std(counts, n=10):
    tz_list = Counter(counts)
    return tz_list.most_common(n)


sort_count = top_counts_std(count_tz_dict)
print(sort_count)