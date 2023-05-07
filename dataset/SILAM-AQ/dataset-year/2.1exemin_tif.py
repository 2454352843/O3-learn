import os,shutil
import glob
from datetime import date, timedelta, datetime
import tqdm
'''
检验: 在第二步tif文件夹内进行操作
      修改文件名字，与自己的日期和小时对应，并由utc时间修改为北京时间
      最后再次检验是否有文件缺失
'''

floder = r'F:\data\xyz-O3\GEOS-CF\workspace\weather\2tif'
output_folder = r'F:\data\xyz-O3\SILAM\workspace\21tif'
utc_folder = r'F:\data\xyz-O3\SILAM\workspace\22tif'


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
    #     SILAM-AQ-china_v5_5_1_2022102900_019_4.tif
    for tif in tifs:
        if (len(os.path.basename(tif)) < 41):
            continue

        hour_int = int(tif[-8:-6]) + int(tif[-5:-4]) - 1
        if (hour_int < 24):
            new_name = os.path.basename(tif)[:-12] + f'_{hour_int}.tif'
        elif (hour_int < 24 * 2):
            hour = hour_int - 24
            date = datetime.strftime(datetime.strptime(tif[-20:-12], "%Y%m%d") + timedelta(days=1), '%Y%m%d')
            new_name = os.path.basename(tif)[:-20] + f'{date}_{hour}.tif'
            if (hour > 0):
                print(f'tif new_name:{new_name}')
        elif (hour_int < 24 * 3):
            hour = hour_int - 24 * 2
            date = datetime.strftime(datetime.strptime(tif[-20:-12], "%Y%m%d") + timedelta(days=2), '%Y%m%d')
            new_name = os.path.basename(tif)[:-20] + f'{date}_{hour}.tif'
            print(f'tif new_name:{new_name}')
        elif (hour_int < 24 * 4):
            hour = hour_int - 24 * 3
            date = datetime.strftime(datetime.strptime(tif[-20:-12], "%Y%m%d") + timedelta(days=3), '%Y%m%d')
            new_name = os.path.basename(tif)[:-20] + f'{date}_{hour}.tif'
            print(f'tif new_name:{new_name}')
        elif (hour_int < 24 * 5):
            hour = hour_int - 24 * 4
            date = datetime.strftime(datetime.strptime(tif[-20:-12], "%Y%m%d") + timedelta(days=4), '%Y%m%d')
            new_name = os.path.basename(tif)[:-20] + f'{date}_{hour}.tif'
            print(f'tif new_name:{new_name}')

        # 调用改名函数，完成改名操作
        try:
            # os.rename(tif, os.path.split(tif)[0] + os.path.sep + new_name)
            shutil.copy(tif,output_folder+ os.path.sep + new_name)
        except Exception:
            print(Exception)
    print('运行结束')


# 第二步  utc时间转换
def utc_rename():
    tifs = glob.glob(output_folder + os.path.sep + '*.tif')

    # 文件名替换
    #     SILAM-AQ-china_v5_5_1_2022102900_019_4.tif
    for tif in tifs:
        date = (os.path.basename(tif).split('_')[4])
        time = os.path.basename(tif).split('_')[5].split('.')[0]
        time = '0' + time if int(time) < 10 else time
        dtime = datetime.strftime(datetime.strptime(date + time, "%Y%m%d%H") + timedelta(hours=8), '%Y%m%d-%H')

        new_date,new_time = dtime.split('-')[0],dtime.split('-')[1]
        # 'E:\\data\\3. SILAM\\workspace\\2tif\\SILAM-AQ-china_v5_5_1_20221013_1.tif'

        new_name =utc_folder + os.path.sep + os.path.basename(tif)[:22]+f'{new_date}_{new_time}.tif'
        # 调用改名函数，完成改名操作
        try:
            shutil.copy(tif, new_name)
        except Exception:
            print(Exception)

    print('运行结束!')


def main():
    rename()

    utc_rename()

if __name__ == '__main__':
    main()

    # a = r'SILAM-AQ-china_v5_5_1_2022102900_019_4.tif'
    # print(len(a))
