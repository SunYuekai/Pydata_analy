# coding:utf-8

import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict
from collections import Counter
from pandas import DataFrame, Series

# 创建用户字段名称列表
unames = ['user_id','gender','age','occupation','zip']
# 读取dat类型文件 分隔符为::
users = pd.read_table('data/users.dat', sep="::", header=None, names=unames)
# 创建评分字段名称列表
rnames = ['user_id','movie_id', 'rating', 'timestamp']
ratings = pd.read_table('data/ratings.dat', sep="::", header=None, names=rnames)
# 创建电影字段名称列表
mnames = ['movie_id', 'title', 'genres']
movies = pd.read_table('data/movies.dat', sep="::", header=None, names=mnames)
# 合并DF
data = pd.merge(users, pd.merge(ratings, movies))
# 对data按照年龄 电影名称进行分组 计算评分均值
mean_ratings = data.pivot_table(values='rating', index='title', columns='gender', aggfunc='mean')
print(mean_ratings[:2])
# 过滤掉评分数据不够250条的数据 返回Series对象 标签为分组值 对应元素为size条数
ratings_by_title = data.groupby('title').size()
print(ratings_by_title)
# 开始过滤
active_titles = ratings_by_title.index[ratings_by_title >= 250]
# 获取对应行从DF中 传入一个Series 过滤掉数量小于250的data行记录
mean_ratings = mean_ratings.ix[active_titles]  # 对应index中第一个索引
# 获取女性最喜欢的电影
top_female_ratings = mean_ratings.sort_values(by='F', ascending=False)  # 降序排列
print(top_female_ratings[:10])
# 计算评分分歧 添加新的列标记diff
top_female_ratings['diff'] = top_female_ratings['F'] - top_female_ratings['M']
# 对diff列值进行排序 并倒序 [i:j:s] 当步长s为-1 i和j 默认为-1 到-len(list)-1 即倒序复制列表
print(top_female_ratings[:2])
sorted_by_diff = top_female_ratings.sort_values('diff')
print(sorted_by_diff[::-1][:10])





