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
# 获取agent 数据 dropna()去除空值列 否则split会抛出异常
results = Series([x.split()[0] for x in frame.a.dropna()])
cframe = frame[frame.a.notnull()]  # 返回frame对象 a列值为空的行记录删除
operating_system = np.where(cframe['a'].str.contains('Windows'),'Windows','No windwos')
print(operating_system[:5])
by_tz_os = cframe.groupby(['tz', Series(operating_system)])  # [分组字段,分组字段对应拆分类别值数组或序列]
agg_count= by_tz_os.size().unstack().fillna(0)  #DF对象
print(agg_count[:10])
# 获取间接索引数组 用于按照升序排列 按照sum(1)排名进行索引重排序
indexer = agg_count.sum(1).argsort()
count_subset = agg_count.take(indexer)[-10:]
print(type(count_subset))
# count_subset.plot(kind='barh', stacked=True)
normed_subset = count_subset.div(count_subset.sum(1), axis=0)  # 以百分比显示 axis维度选择
normed_subset.plot(kind='barh', stacked=True)
plt.show()
