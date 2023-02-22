import os
import sys
import random
import threading
import multiprocessing
import time

# 线程执行函数
def worker(procnum, return_dict):
    """worker function"""
    print(str(procnum) + " represent!")
    num = random.randint(5, 20)
    arr = []
    for i in range(num):
        arr.append(i)
    # 依据线程id来存储各线程对应的处理结果
    time.sleep(10)
    return_dict[procnum] = (procnum, arr)


if __name__ == "__main__":
    manager = multiprocessing.Manager()
    # 构造返回值存储结构，本质是共享内存方式
    return_dict = manager.dict()
    jobs = []
    for i in range(5):
        # 将构造的返回值存储结构传递给多线程执行函数，并标识各个线程id
        p = multiprocessing.Process(target=worker, args=(i, return_dict))
        jobs.append(p)
        p.start()

    for proc in jobs:
        proc.join()

    # 所有线程处理完毕后，遍历结果输出
    for id, arr in return_dict.values():
        print(id, arr)