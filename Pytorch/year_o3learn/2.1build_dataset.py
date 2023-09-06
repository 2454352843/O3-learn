import datetime
import os
import random

import gdal
import numpy as np
import pandas as pd
import glob
from tqdm import tqdm
from Pytorch.year_o3learn.Resource import config
from Pytorch.year_o3learn.utils import Gdaltiff

train_ratio = 0.9
test_ratio = 1 - train_ratio
rootdata = config.base_path
# tif_list = config.tif_list


'''
构建数据集
修改： 1. 构建白天13小时数据集  2. 只使用华北平原地区的数据
'''
data_list, train_list, test_list = [], [], []
len_list = 0


# 记录数据构建日志
def setlog(line):
    txt_path = r'D:\work\python\pycharm\O3-learn\Pytorch\year_o3learn\Resource\dataset_log.txt'
    with open(txt_path, 'a', encoding='UTF-8') as f:
        f.write(str(line + '\n'))


def get_tiflist(dir):
    map = {}
    # 读取landcover
    if (dir == 'LandCover'):
        # 读取辅助数据
        other_files = glob.glob(rootdata + os.path.sep + 'LandCover//*.tif')
        # 读取ndvi
        for root, dirs, files in os.walk(rootdata + os.path.sep + 'LandCover//NDVI'):
            if (len(files) == 0):
                continue
            list = []
            date = root.split(os.path.sep)[-1]
            for file_i in files:
                if 'tif' in file_i[-4:]:
                    list.append(root + os.path.sep + file_i)
            map[date] = list + other_files

    else:  # 读取其他文件
        for root, dirs, files in os.walk(rootdata + os.path.sep + dir):
            if (len(files) == 0):
                continue
            list = []
            date = root.split(os.path.sep)[-1]
            for file_i in files:
                if 'tif' in file_i[-4:]:
                    list.append(root + os.path.sep + file_i)
            map[date] = list

    # print(map)train_tf
    # map.pop(dir)
    return map


# 构建测试集、训练集
def main():
    xlsxfiles = glob.glob(rootdata + os.path.sep + 'Site' + os.path.sep + "*.xlsx")
    global len_list

    # 1.获取全部数据
    filesMap = {}
    tif_list = config.tif_list

    for i in tif_list:
        filesMap[i] = get_tiflist(i)

    # print(filesMap)

    # 2.根据日期读取数据
    for i in tqdm(range(len(xlsxfiles))):

        xlsxfile = xlsxfiles[i]
        # print(xlsxfile.split(os.path.sep)[-1])
        date = xlsxfile.split(os.path.sep)[-1][:-5].replace('-', '_')
        # s_date = datetime.datetime.strptime(date, '%Y_%m_%d')
        # v_date = datetime.datetime.strptime('2022_04_09', '%Y_%m_%d')
        # if (int((v_date - s_date).days) > 0):
        #     continue

        df = pd.read_excel(xlsxfile)

        # 3.读取 10- 19点数据，共10个小时
        for i in range(13):

            # 记录每小时的数据
            time = i + 8
            data_list = []
            # 4. 读取地面站点数据
            if (time < 10):
                time = '0' + str(time)
            else:
                time = str(time)

            save_path = r'Resource/databytime/{n}.txt'.format(n=date + '_' + time)
            if os.path.exists(save_path):
                continue

            if (int(date.split('_')[1]) >= 6 and int(date.split('_')[1]) < 10):

                df1 = df[df['Time'] == f'{time}:00:00']  # 6-9月修改后的数据用这个
            else:
                df1 = df[df['Time'] == f'{time}:00:00.0000000']  # 正常数据用这个

            Latlist = df1['Latitude'].reset_index(drop=True)
            Lonlist = df1['Longitude'].reset_index(drop=True)
            O3list = df1['O3'].reset_index(drop=True)

            # 5. 筛选读取改时间点对应的文件
            list_str = []
            if not date in filesMap['GEOS'].keys():
                continue
            for k in filesMap['GEOS'][date]:
                if (time in k[-7:] and 'O3' not in k):
                    # print(Timelist[j][:2])
                    # print(k[-7:])
                    list_str.append(k)

            if not date in filesMap['SILAM'].keys():
                continue
            for k in filesMap['SILAM'][date]:
                if time in k[-6:]:
                    list_str.append(k)

            if not date in filesMap['Tropomi'].keys():
                continue
            for k in filesMap['Tropomi'][date]:
                if not 'temp' in k:
                    list_str.append(k)

            # 筛选landcover
            dates = list(filesMap['LandCover'].keys())
            # 确定NDVI数据时间
            date_r = dates[0]
            for i in range(len(date_r) - 1):
                date_i = dates[i + 1]
                second_date = datetime.datetime.strptime(date_i, '%Y_%m_%d')
                first_date = datetime.datetime.strptime(date_r, '%Y_%m_%d')
                date_value = datetime.datetime.strptime(date, '%Y_%m_%d')
                date_r = date_r if abs(int((first_date - date_value).days)) < abs(
                    int((second_date - date_value).days)) else date_i

            for k in filesMap['LandCover'][date_r]:
                if not 'temp' in k:
                    list_str.append(k)

            # 如果缺少数据，则跳到下一条数据
            if len(list_str) < 11:
                list1 = []
                arr = config.arr_list
                for value in arr:
                    mark = 0
                    for i in list_str:
                        if value in i:
                            mark = 1
                            break
                    if mark == 0:
                        list1.append(value)

                line = f"{date}_{time}  缺少{11 - len(list_str)}个数据,缺少的数据为：{list1}"
                setlog(line)
                continue

            # 6. 打开读取对应的文件
            tif_list = []
            arr_list = config.arr_list
            for i in range(len(arr_list)):
                for path in list_str:
                    if arr_list[i] in path:
                        tif_list.append(Gdaltiff(path))

            # print(len(tif_list))

            # 7. 生成数据集

            for j in range(len(Latlist)):
                lat = str(round(Latlist[j], 2))
                lon = str(round(Lonlist[j], 2))

                # 筛选华北平原对应的数据 北纬(lat)32°～40°，东经(long)114°～121°   big:lon 107-124 lat 28-45
                if not (float(lat) < 45.00 and float(lat) > 28.00):
                    continue
                if not (float(lon) < 124.00 and float(lon) > 107.00):
                    continue

                point = {'lat': lat,
                         'lon': lon}
                # data = (lat if len(lat.split('.')[-1])>=2 else lat + '0') + '\t' +(lon if len(lon.split('.')[-1]) >= 2 else lon + '0') + '\t' + date + '\t' + Timelist[j] + '\t' + str(O3list[j])
                line = (lat if len(lat.split('.')[-1]) >= 2 else lat + '0') + '\t' + (
                    lon if len(lon.split('.')[-1]) >= 2 else lon + '0') + '\t' + date + '\t' + time + '\t' + str(
                    O3list[j])

                for k in range(len(tif_list)):
                    tif = tif_list[k]
                    arr_value = tif.getImg(point)
                    arr_value = np.reshape(arr_value, (1, config.img_size[0] * config.img_size[1])).tolist()
                    line = line + '\t' + str(arr_value[0])

                line = line + '\n'
                data_list.append(line)

            # 8.保存每小时的数据

            with open(save_path, 'w', encoding='UTF-8') as f:
                for line in data_list:
                    f.write(str(line))

        # print(date_list)


def shuffle():
    #  读取数据
    data_list = []
    txt_path = r'Resource/databytime'
    file_list = glob.glob(txt_path + '/*.txt')
    for path in file_list:
        with open(path, 'r', encoding='utf-8') as f:
            imgs_info = f.readlines()
            data_list = data_list + imgs_info

    #  构建测试集 训练集
    random.shuffle(data_list)
    for i in range(0, int(len(data_list) * train_ratio)):
        train_list.append(data_list[i])

    for i in range(int(len(data_list) * train_ratio), len(data_list)):
        test_list.append(data_list[i])

    #  读出数据集为文本格式
    with open('Resource/train3.txt', 'w', encoding='UTF-8') as f:
        for train_img in train_list:
            f.write(str(train_img))

    with open('Resource/test3.txt', 'w', encoding='UTF-8') as f:
        for test_img in test_list:
            f.write(test_img)


if __name__ == '__main__':
    main()
    print("共有 {n} 条数据".format(n=len_list))
    shuffle()
