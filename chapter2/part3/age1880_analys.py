# coding:utf-8

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 读取1880出生婴儿文件
names1880 = pd.read_csv('../../dataset/babynames/yob1880.txt', names=[
    'name', 'sex','births'])
pieces = []
columns = ['name', 'sex', 'births']
years = range(1880, 2011)

for year in years:
    path = '../../dataset/babynames/yob%s.txt' % year
    frame = pd.read_csv(path, names=columns)
    frame['year'] = year
    pieces.append(frame)
# 将列表中的DF忽略index进行拼接
names = pd.concat(pieces,ignore_index=True)
# 对names根据sex和year分组对births进行聚合
total_births = names.pivot_table('births', index='year', columns='sex', aggfunc='sum')


# 添加列prop 根据函数
def add_prop(group):
    group['prop'] = group.births/group.births.sum()
    return group


# 有效值检查 不改变原DF 需要接收返回值
names = names.groupby(['year', 'sex']).apply(add_prop)
# print(names[:10])
# print(names.prop.sum())


# 取出每对分组中births排名前1000的值
def get_top1000(group):
    return group.sort_index(by='births', ascending=False)[:1000]


# top_1000_g_names.index names=['year', 'sex', None]
top_1000_g_names = names.groupby(['year', 'sex']).apply(get_top1000)
#  DIY将分块DF进行合并
pieces = []
for col_tuple, group in names.groupby(['year', 'sex']):
    pieces.append(group.sort_values('births', ascending=False)[:1000])
top_1000 = pd.concat(pieces,ignore_index=True)
# 取男孩和女孩DF
boys = top_1000[top_1000['sex'] == 'M']
girs = top_1000[top_1000['sex'] == 'F']
total_births = top_1000.pivot_table('births',
                                    index='year',
                                    columns='name',
                                    aggfunc=sum)
# 绘图 取name为J H
subset = total_births[['John', 'Harry']]
# print(subset[:10])
subset.plot(subplots=False, figsize=(12, 10), grid=False,
            title='Number of births per year')
# 计算流行度
table = top_1000.pivot_table('prop', index='year',
                             columns='sex',
                             aggfunc=sum)
table.plot(title='Sum of table1000.pop by year and sex'
           , yticks=np.linspace(0, 1.2, 13),
           xticks=range(1880, 2020, 10))


# 根据year sex分组 获取排名前50%的名字个数
def get_quantile_count(group, q=0.5):
    group = group.sort_index(by='prop', ascending=False)
    return int(group.prop.cumsum().searchsorted(q)+1)


diversity = top_1000.groupby(['year', 'sex']).apply(get_quantile_count)
# unstack(列索引名称) 重新将DF  reshape
diversity = diversity.unstack('sex')
# 将多样性绘图 每年男 女起名前50的概率的名称个数(top1000) 行索引为横坐标 列索引为绘图分类 默认
diversity.plot(title='Number of popular names in top 50%')

# 最后一个字母统计 定义map函数
last_letters = names.name.map(lambda x: x[-1])
last_letters.name = 'last_letter'
table = names.pivot_table('births', index=last_letters,
                          columns=['sex', 'year'], aggfunc=sum)
subtable = table.reindex(columns=[1910, 1960, 2010], level='year')
# print(subtable.head())
# sum时将DF看作二维表 按照列字段多维索引的最高维度进行sum
# print(subtable.sum())
letter_prop = subtable/subtable.sum().astype(float)
# 统计字母结尾 按照每年每个性别分组 占总字母的比例
# print(letter_prop.head())
# fig为图形对象 axes为轴对象 2,1位置构成了两个ax对象
fig, axes = plt.subplots(2, 1, figsize=(100, 8))
# 柱状图 ax选择对应位置的柱状图 行索引为横坐标 列索引为柱分类 【''】只能获取最外层的索引
letter_prop['M'].plot(kind='bar', rot=0, ax=axes[0], title='Male')
letter_prop['F'].plot(kind='bar', rot=0, ax=axes[1], title='Female')
# plt.show()
letter_prop = table / table.sum()
# ix ix支持字符与整数索引 [行索引列表] 最外层列索引 获得二维DF .T转置 转置为了使时间为横坐标
dny_ts = letter_prop.ix[['d', 'n', 'y'], 'M'].T
# 默认折线图
dny_ts.plot()
# 绘制折线图 每年每个性别以lesl开头的名字
# 获得name序列
all_names = top_1000.name.unique()
# 获取标记数组
mask = np.array(['lesl' in x.lower() for x in all_names])
# 根据mask标记数组过滤序列
lely_like = all_names[mask]
# 根据得到的lely_like过滤列索引DF.列索引.isin([索引序列]) 根据某一列的过滤序列过滤值
filtered = top_1000[top_1000.name.isin(lely_like)]
# 根据过滤后的DF 根据name分组查看某一列的sum值 返回序列
# print(filtered.groupby('name').births.sum())
# print(type(filtered.groupby('name').births.sum()))
# 根据过滤后的DF 分组统计值 并绘图
table = filtered.pivot_table('births',index='year',
                             columns='sex', aggfunc='sum')
# 折线图y值规范化 div 取概率
print(table[:10])
# sum(1) 1->根据行索引进行sum返回序列
print(table.sum(1))
table = table.div(table.sum(1), axis=0)
print(table[:10])
# 绘制折线图
table.plot(style={'M': 'k-', 'F': 'k--'})
plt.show()









