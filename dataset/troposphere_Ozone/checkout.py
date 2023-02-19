import os

basepath = r'E:\data\1. S5P_OFFL_L2_O3\20220501-20220930'
file = r'D:\work\python\data\nc\subset_S5P_L2__O3__PR_HiR_2_20221012_064304.txt'
checkpath = 'check.txt'

def checkout():
    # 删除文件大小不对的文件和后缀不对的文件
    # 删除重复文件

    mark = 0
    list = os.listdir(basepath)
    count = 0
    for i in list:

        count += 1
        path = basepath + os.path.sep + i
        if not ("nc" in path):
            os.remove(path)
            continue

            
        if '(' in i:
            os.remove(path)
            continue

        size = os.stat(path).st_size
        if (size < 378880000):
            try:
                os.remove(path)
            except Exception:
                print(Exception)
            finally:
                mark = -1
    if (mark < 0):
        return -1


def file_checkout():
    f = open(file)
    list = os.listdir(basepath)

    # 读取一行数据
    for line in f:
        filename = line.split('/')[-1]
        mark = 0
        for i in list:
            if i in filename:
                mark =1
                break
        if mark == 0:
            checkfile = open(checkpath, 'a')
            print(line)
            checkfile.write(line)



        mark += 1



file_checkout()
# checkout()
