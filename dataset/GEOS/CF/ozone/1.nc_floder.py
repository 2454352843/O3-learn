import glob
import os, shutil
from datetime import date, timedelta, datetime

# 构建nc文件夹  确保silam数据连贯，切数据无异常

input_floder = r'F:\data\xyz-O3\GEOS-CF\O3'
output_floder = r'F:\data\xyz-O3\GEOS-CF\workspace\ozone\1nc'


def mycopyfile(srcfile, dstpath):  # 复制函数
    if not os.path.isfile(srcfile):
        print("%s not exist!" % (srcfile))
    else:
        fpath, fname = os.path.split(srcfile)  # 分离文件名和路径
        if not os.path.exists(dstpath):
            os.makedirs(dstpath)  # 创建路径
        new_name = dstpath + os.path.sep + fname
        if os.path.exists(new_name):
            print(f'{new_name}已经存在') # 创建路径
            return
        shutil.copy(srcfile, new_name)  # 复制文件
        print("copy %s -> %s" % (srcfile, new_name))


# 文件检验： 判断2023年4月之前的文件是否完整
def examine(list):
    pass


def get_floder():
    # 文件读取
    list_nc = glob.glob(input_floder + os.path.sep + '*.nc*')

    list_out = []
    for i in range(300):

        # 日期生成
        strTime = datetime.strptime('2023-03-15-12', "%Y-%m-%d-%H")
        date = (strTime + timedelta(days=-i))
        strdate = datetime.strftime(date, '%Y%m%d')
        # print(date)
        if (int(strdate) < 20221001):
            break

        # 每日文件筛选
        list_day = []
        for file in list_nc:
            path, basename = os.path.split(file)
            if (strdate in basename[:52]):
                list_day.append(file)

        mark = 0
        for i in range(24):

            timeValue = date + timedelta(hours=i)
            strtime1 = datetime.strftime(timeValue, '%Y%m%d_%H')
            mark_hour = 0 # 判断该小时是否有数据
            for file in list_day:
                path, basename = os.path.split(file)
                if(strtime1 in basename[50:]):
                    list_out.append(file)
                    mark_hour = 1
                    break

            if(mark_hour == 0):
                print(f'{strtime1} 没有数据!!!')



    print(len(list_out))

    for i in range(len(list_out)):
        mycopyfile(list_out[i], output_floder)

    # 文件筛选


def main():
    get_floder()


if __name__ == '__main__':
    main()
