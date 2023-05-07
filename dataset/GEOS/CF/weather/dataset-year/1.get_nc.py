import glob
import os, shutil
from datetime import date, timedelta, datetime

# 构建nc文件夹  确保数据连贯，切数据无异常

input_floder = r'F:\data\xyz-O3\GEOS-CF\weather'
output_floder = r'F:\data\xyz-O3\GEOS-CF\workspace\weather\1nc'


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
            file_path, file_name = os.path.split(file)
            if (date in file_name.split('.')[4][:10]):
                list_day.append(file)

        mark = 0
        time_c = datetime.strptime(date + '12', "%Y%m%d%H")
        for hour in range(24):
            date_c = (time_c + timedelta(hours=hour))
            date_c = datetime.strftime(date_c, '%Y%m%d_%H')
            for file_c in list_day:
                file_path, file_name = os.path.split(file_c)
                if (date_c in file_name.split('.')[4][9:]):
                    list_out.append(file_c)
                    mark = 1
            if (mark == 0):
                print(f'{date}_{date_c} 不存在')
                mark = 0
                # for count_i  in  range(4):
                #     strTime_i = datetime.strptime(date, "%Y%m%d")
                #     date_i = (strTime + timedelta(days=-count_i))
                #     date_i = datetime.strftime(date_i, '%Y%m%d')
                #     file_path, file_name = os.path.split(file)
                #     if (date_i in file_name.split('.')[4][:10]):
                #

    print(len(list_out))

    for i in range(len(list_out)):
        mycopyfile(list_out[i], output_floder)

    # 文件筛选


def main():
    get_floder()


if __name__ == '__main__':
    main()
