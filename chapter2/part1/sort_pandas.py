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
# 使用pandas进行数据排序
frame = DataFrame(records)
# print(frame['tz'].value_counts())
# 进行图形展示 1.填充空值 2.填充''未知值
frame_series = frame['tz'].fillna('Missing')
frame_series[frame_series == ''] = 'Unknown'
#print(frame_series.value_counts())
# 进行图形展示

frame_series.value_counts()[:10].plot(kind='barh', rot=0)
# plt.show()
# 删除缺失数据
frame.a.dropna()
print(frame.shape)
print(frame[frame.a.notnull()].shape)


