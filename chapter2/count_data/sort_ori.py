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


# 使用源生类库计数
def count_data(data):
    count = {}
    for key in data:
        if key in count:
            count[key] +=1
        else:
            count[key] = 0
    return count


count_tz = count_data([rz['tz'] for rz in records if 'tz' in rz])


# 获取排名 字典{tz,count}->列表[(value:tz),(value,tz)] 换成{}不排序
def top_counts(counts, n=20):
    tz_list = [(value, key)for key, value in counts.items()]
    tz_list.sort()
    return tz_list[-n:]


sort_count1 = top_counts(count_tz)
print(sort_count1)