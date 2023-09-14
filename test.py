import os,shutil
import signal
import time

import multitasking
signal.signal(signal.SIGINT, multitasking.killall)
multitasking.set_max_threads(3)  # 最大线程数为3
'''
将检验后的数据移动到数据集中
只需要移动10点-19点的数据（10个小时）
'''
map1 = {}
for i in range(3):
    map = {}
    map[f'1{i}'] = [1,2,3]
    map1[f'1{i}'] = map


len1 = len(map1.keys())
ll = list(map1.keys())
print(ll[0])
for i in range(len1):
    print(map1[i])