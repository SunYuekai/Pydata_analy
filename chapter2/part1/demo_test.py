# coding:utf-8

import numpy as np
a_list = [1,2,3]
na_list = np.array(a_list)
na_list[na_list == 2] = 10
print(na_list)
