# coding:utf-8

import pandas as pd


obj3 = pd.Series(['blue', 'purple', 'yellow'], index=[0, 2, 4])
print(obj3.reindex(range(6), method='bfill')
)