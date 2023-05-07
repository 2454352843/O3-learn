import os, shutil
import glob
from datetime import date, timedelta, datetime
import tqdm

'''
检验: 在第二步tif文件夹内进行操作
      修改文件名字，与自己的日期和小时对应，并由utc时间修改为北京时间
      最后再次检验是否有文件缺失
'''

floder = r'H:\data\xyz-O3\GEOS-CF\workspace\weather\2tif'
output_folder = r'H:\data\xyz-O3\GEOS-CF\workspace\weather\21tif'
utc_folder = r'H:\data\xyz-O3\GEOS-CF\workspace\weather\2tif'


# def examine():
#     tifs = glob.glob(floder+os.path.sep+'*.tif')
#     # print(len(tifs))
#
#     # 日期生成
#     strTime = datetime.strptime('2023-03-31', "%Y-%m-%d")
#     for i in range(300):
#         date = (strTime + timedelta(days=-i))
#         date = datetime.strftime(date, '%Y%m%d')
#
#         if (int(date) < 20221012):
#             break
#
#         mark01 = 0
#         mark07 = 0
#         mark13 = 0
#         mark19 = 0
#         for tif in tifs:
#             # SILAM-AQ-china_v5_5_1_2022102600_019_5.tif
#             if(date in tif):
#                 if('01' in tif[-9:-6]):
#                     mark01 = 1
#                 elif('07' in tif[-9:-6]):
#                     mark07 = 1
#                 elif('13' in tif[-9:-6]):
#                     mark13 = 1
#                 elif('19' in tif[-9:-6]):
#                     mark19 = 1


# 修改文件名 第一步
def rename():
    tifs = glob.glob(floder + os.path.sep + '*.tif')
    # print(len(tifs))

    # 文件名替换
    #     GEOS-CF_20221009_12z+20221009_1230z_PS.tif
    for tif in tifs:
        # if (len(os.path.basename(tif)) < 41):
        #     continue

        basepath, basename = os.path.split(tif)
        new_name = basename.split('_')[0] + '_' + basename.split('_')[2][4:] + '_' + basename.split('_')[3][:-1] + '_' + \
                   basename.split('_')[4]

        # 调用改名函数，完成改名操作
        try:
            # os.rename(tif, os.path.split(tif)[0] + os.path.sep + new_name)
            shutil.move(tif, output_folder + os.path.sep + new_name)
        except Exception as e:
            print(e)
    print('运行结束')


# 第二步  utc时间转换
def utc_rename():
    tifs = glob.glob(output_folder + os.path.sep + '*.tif')

    # 文件名替换
    #     GEOS-CF_20221009_1230_PS.tif
    for tif in tifs:
        date = (os.path.basename(tif).split('_')[-3])
        time = os.path.basename(tif).split('_')[-2][:2]

        dtime = datetime.strftime(datetime.strptime(date + time, "%Y%m%d%H") + timedelta(hours=8), '%Y%m%d-%H')

        new_date, new_time = dtime.split('-')[0], dtime.split('-')[1]
        # 'E:\\data\\3. SILAM\\workspace\\2tif\\SILAM-AQ-china_v5_5_1_20221013_1.tif'

        new_name = utc_folder + os.path.sep + os.path.basename(tif).split('_')[0] + f'_{new_date}_{new_time}_'+os.path.basename(tif).split('_')[-1]
        # 调用改名函数，完成改名操作
        try:
            shutil.move(tif, new_name)
        except Exception:
            print(Exception)

    print('运行结束!')


def main():
    # rename()

    utc_rename()


if __name__ == '__main__':
    main()

    # a = r'SILAM-AQ-china_v5_5_1_2022102900_019_4.tif'
    # print(len(a))
