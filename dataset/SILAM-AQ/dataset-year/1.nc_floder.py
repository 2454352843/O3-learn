import glob
import os, shutil
from datetime import date, timedelta, datetime

# 构建nc文件夹  确保silam数据连贯，切数据无异常

input_floder = r'E:\data\3. SILAM\silam_china_v5_5_1'
output_floder = r'E:\data\3. SILAM\workspace\1nc'


def mycopyfile(srcfile, dstpath):  # 复制函数
    if not os.path.isfile(srcfile):
        print("%s not exist!" % (srcfile))
    else:
        fpath, fname = os.path.split(srcfile)  # 分离文件名和路径
        if not os.path.exists(dstpath):
            os.makedirs(dstpath)  # 创建路径
        shutil.copy(srcfile, dstpath + os.path.sep + fname)  # 复制文件
        print("copy %s -> %s" % (srcfile, dstpath + fname))


# 文件检验： 判断2023年4月之前的文件是否完整
def examine(list):
    pass


def get_floder():
    # 文件读取
    list_nc = glob.glob(input_floder + os.path.sep + '*.nc*')

    list_out = []
    for i in range(300):

        # 日期生成
        strTime = datetime.strptime('2023-03-31', "%Y-%m-%d")
        date = (strTime + timedelta(days=-i))
        date = datetime.strftime(date, '%Y%m%d')
        # print(date)
        if (int(date) < 20221001):
            break

        # 每日文件筛选
        list_day = []
        for file in list_nc:
            if (date in file):
                list_day.append(file)

        mark = 0
        for file in list_day:
            if ('_001' in file):
                list_out.append(file)
                mark = 1
        if (mark == 0):
            print(f'{date}_001不存在')
            mark = 0

        for file in list_day:
            mark = 1
            if ('_007' in file):
                list_out.append(file)
                mark = 1
        if (mark == 0):
            mark = 0
            print(f'{date}_007不存在')

        for file in list_day:
            if ('_013' in file):
                list_out.append(file)
                mark = 1
        if (mark == 0):
            mark = 0
            print(f'{date}_013不存在')

        for file in list_day:
            if ('_019' in file):
                list_out.append(file)
                mark = 1
        if (mark == 0):
            mark = 0
            print(f'{date}_019不存在')

    print(len(list_out))

    for i in range(len(list_out)):
        mycopyfile(list_out[i], output_floder)

    # 文件筛选


def main():
    get_floder()


if __name__ == '__main__':
    main()
