import os
import random

import gdal
import numpy as np
import pandas as pd
import glob
from tqdm import tqdm
from Pytorch.O3_estimate.Resource import config

train_ratio = 0.9
test_ratio = 1 - train_ratio
rootdata = config.base_path
# tif_list = config.tif_list


data_list, train_list, test_list = [], [], []
len_list = 0


# tiff加载类
class Gdaltiff():
    def __init__(self, path):
        self.path = path
        ds = gdal.Open(path)

        self.rows = ds.RasterYSize  # 行数
        self.cols = ds.RasterXSize  # 列数
        self.bands = ds.RasterCount
        self.Proj = ds.GetProjection()
        self.Transform = ds.GetGeoTransform()
        self.Bandarr = ds.GetRasterBand(1).ReadAsArray()
        # print(Bandarr.shape)
        del ds

        self.maxLatmain = self.Transform[3]
        # minLatmain = Transform[3] + rows * Transform[5]
        self.minLonmain = self.Transform[0]
        # maxLonmain = Transform[0] + cols * Transform[1]

    # 根据经纬度读取对应数据
    def getImg(self, point):
        ratio = config.ratio
        x, y = config.img_size
        lat = float(point['lat'])
        lon = float(point['lon'])

        lat_value = int((self.maxLatmain - (lat)) / ratio)
        lon_value = int((lon - self.minLonmain) / ratio)

        # y_min = lat_value - int(y / 2)
        # y_max = y_min + y

        y_left = lat_value - int(y / 2)
        y_right = y_left + y

        x_left = lon_value - int(x / 2)
        x_right = x_left + x

        data = self.Bandarr[y_left:y_right, x_left:x_right]

        getdata = lambda x: self.Bandarr[lat_value - x: lat_value + x, lon_value - x:lon_value + x]
        # 如果数据在边缘位置 需要进行数组扩充
        if (x_left < 0):
            if (y_left < 0):
                value = lon_value if lon_value < lat_value else lat_value
            else:
                value = lon_value if lon_value < self.rows - 1 - lat_value else self.rows - 1 - lat_value
            data = getdata(value)
            return data

        if (y_left < 0):
            value = lat_value if lat_value < self.cols - 1 - lon_value else self.cols - 1 - lon_value
            data = getdata(value)
            return data

        if (y_right > self.rows - 1):
            if (x_right > self.cols - 1):
                value = self.rows - 1 - lat_value if self.rows - 1 - lat_value < self.cols - 1 - lon_value else self.cols - 1 - lon_value
            else:
                value = self.rows - 1 - lat_value if self.rows - 1 - lat_value < lon_value else lon_value
            data = getdata(value)
            return data

        if (x_right > self.cols - 1):
            value = self.cols - 1 - lon_value if self.cols - 1 - lon_value < lat_value else lat_value
            data = getdata(value)
            return data
        # data = Bandarr[0, :]

        return data

    def __str__(self):
        return self.path


def get_tiflist(dir):
    map = {}
    for root, dirs, files in os.walk(rootdata + os.path.sep + dir):
        list = []
        date = root.split(os.path.sep)[-1]
        for file_i in files:
            if 'tif' in file_i[-4:]:
                list.append(root + os.path.sep + file_i)
        map[date] = list

    # print(map)train_tf
    map.pop(dir)
    return map


# 构建测试集、训练集
def main():
    xlsxfiles = glob.glob(rootdata + os.path.sep + 'Site-xlsx' + os.path.sep + "*.xlsx")
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
        df = pd.read_excel(xlsxfile)

        # 3.读取每小时数据
        for time in range(24):
            # 记录每小时的数据
            data_list = []
            # 4. 读取地面站点数据
            if (time < 10):
                time = '0' + str(time)
            else:
                time = str(time)

            df1 = df[df['Time'] == f'{time}:00:00.0000000']

            Latlist = df1.values[:, 1]
            Lonlist = df1.values[:, 2]
            O3list = df1.values[:, 6]

            # 5. 筛选读取改时间点对应的文件
            list_str = []
            for k in filesMap['GEOS'][date]:
                if time in k[-7:]:
                    # print(Timelist[j][:2])
                    # print(k[-7:])
                    list_str.append(k)

            for k in filesMap['SILAM'][date]:
                if time in k[-6:]:
                    list_str.append(k)

            for k in filesMap['Tropomi'][date]:
                if not 'temp' in k:
                    list_str.append(k)

            if int(date[-2:]) <= 17:

                for k in filesMap['LandCover'][date[:-2] + '09']:
                    if ('resample' in k):
                        continue
                    list_str.append(k)
            else:
                for k in filesMap['LandCover'][date[:-2] + '25']:
                    if ('resample' in k):
                        continue
                    list_str.append(k)

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
                point = {'lat': lat,
                         'lon': lon}
                # data = (lat if len(lat.split('.')[-1])>=2 else lat + '0') + '\t' +(lon if len(lon.split('.')[-1]) >= 2 else lon + '0') + '\t' + date + '\t' + Timelist[j] + '\t' + str(O3list[j])
                line = (lat if len(lat.split('.')[-1]) >= 2 else lat + '0') + '\t' + (
                    lon if len(lon.split('.')[-1]) >= 2 else lon + '0') + '\t' + date + '\t' + time + '\t' + str(
                    O3list[j])

                for k in range(len(tif_list)):
                    tif = tif_list[k]
                    arr_value = tif.getImg(point)
                    arr_value = np.reshape(arr_value,(1,config.img_size[0]*config.img_size[1])).tolist()
                    line = line + '\t' + str(arr_value[0])


                line = line + '\n'
                data_list.append(line)

            # 8.保存每小时的数据
            save_path = r'Resource/{n}.txt'.format(n = date+'_'+time)
            with open(save_path, 'w', encoding='UTF-8') as f:
                for line in data_list:
                    f.write(str(line))

        # print(date_list)


def shuffle():
    #  读取数据
    data_list = []
    txt_path = r'Resource/databytime'
    file_list = glob.glob(txt_path+'/*.txt')
    for path  in  file_list:
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
    with open('Resource/train.txt', 'w', encoding='UTF-8') as f:
        for train_img in train_list:
            f.write(str(train_img))

    with open('Resource/test.txt', 'w', encoding='UTF-8') as f:
        for test_img in test_list:
            f.write(test_img)


if __name__ == '__main__':
    # main()
    # print("共有 {n} 条数据".format(n=len_list))
    shuffle()