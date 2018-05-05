# coding:utf-8
# @Author : Big_Apple

import time
import random
import string

col_num = 3
col_type_list = ['int', 'str', 'str', 'int']
col_int = []
col_str = []
table_name = 'Test01'
# 根据字段个数和类型自动生成sql公共部分
common_str = 'INSERT INTO TABLE %s VALUES' % table_name
values_str = '(%s,%s,%s)';


# 获取类型索引
def get_type_index():
    global col_str,col_int
    global col_type_list
    for i, v in enumerate(col_type_list):
        if v == 'int':
            col_int.append(i)
        else:
            col_str.append(i)


# 填充类型索引列表
get_type_index()


def get_insert_sql():
    global common_str,col_type_list
    col_values = []
    for i in range(len(col_type_list)):
        if i in col_int:
            col_values.append(str(random.randint(20, 4000)))
        else:
            s = string.ascii_letters
            r = random.choice(s)
            ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 8))
            col_values.append('\''+ran_str+'\'')
    insert_str = '{0} ({1});\n '.format(common_str, ','.join(col_values))
    return insert_str


start = time.clock()

# 批量生成insert_sql
sql_list = []
for i in range(2000000):
    insert_sql = get_insert_sql()
    sql_list.append(insert_sql)

with open('insert_sql.txt', 'w') as tmp_file:
    for i in sql_list:
        tmp_file.write(i)

end = time.clock()

print('run time is %s' % (end-start))







