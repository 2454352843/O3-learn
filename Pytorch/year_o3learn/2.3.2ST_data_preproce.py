import glob

from osgeo import gdal, gdalconst
import numpy as np
import os
from tqdm import tqdm

from Pytorch.year_o3learn.Utils.ST_utils import *

'''
根据构建的数据集，计算时空数据的最大值最小值
计算 数据集内的 最大值，最小值，归一化，标准差，均值
改: 针对华北平原地区，修改行列号输入
'''
path = r'Resource/ST_math.txt'
rootdata = r"E:\data\5-mouth-dataset"

tif_list = ['Tropomi', 'SILAM']

GEOS = ['PS', 'T2M', 'TROPCOL_O3', 'U2M', 'V2M', 'ZPBL']

LandCover = ['DEM', 'NDVI_resample', 'POP', 'pri_sec.tif']
# LandCover = ['tertiary']


img_list = ['PS', 'T2M', 'TROPCOL_O3', 'U2M', 'V2M', 'ZPBL', 'SILAM', 'Tropomi', 'DEM', 'NDVI', 'POP', 'pri_sec',
            'spatial', 'Date', 'Time']


# rasterlist = []


def normalization(data, max_data, min_data):
    _range = max_data - min_data
    return (data - min_data) / _range


def math_count(inputFilePath, label=''):
    Files = []

    meanlist = []
    stdlist = []

    # 1. 数据读取

    max_data = 0
    min_data = 100000
    for root, dirs, files in os.walk(inputFilePath):
        files = files
        for file in files:
            if os.path.splitext(file)[-1] == '.tif' and label in file:  # 查找.tif文件
                sourcefile = os.path.join(root, file)  # 拼路径
                Files.append(sourcefile)
    # print(Files)

    # 2. 归一化处理
    for file1 in tqdm(Files):
        dataset = gdal.Open(file1, gdalconst.GA_ReadOnly)
        # dataset_geo_trans = dataset.GetGeoTransform()
        # col = dataset.RasterXSize
        # row = dataset.RasterYSize
        raster_data1 = dataset.GetRasterBand(1).ReadAsArray()  # 以数组的形式读取栅格点数据
        raster_data1 = raster_data1[raster_data1 > -1000]  # 排除异常值
        max_data = np.max(raster_data1) if np.max(raster_data1) > max_data else max_data
        min_data = np.min(raster_data1) if np.min(raster_data1) < min_data else min_data

    # 3. 计算标准差，均值
    for file1 in tqdm(Files):
        dataset = gdal.Open(file1, gdalconst.GA_ReadOnly)
        # dataset_geo_trans = dataset.GetGeoTransform()
        # col = dataset.RasterXSize
        # row = dataset.RasterYSize

        raster_data1 = dataset.GetRasterBand(1).ReadAsArray()

        raster_data1[raster_data1 >= 10000000] = max_data
        raster_data1[raster_data1 <= -10000000] = min_data
        raster_data1 = normalization(raster_data1, max_data, min_data)

        meandata = np.nanmean(raster_data1)
        stddata = np.nanstd(raster_data1)
        meanlist.append(meandata)
        stdlist.append(stddata)

    mean_np = np.array(meanlist)
    std_np = np.array(stdlist)

    print(f"max value : {max_data}")
    print(f"min value : {min_data}")
    mean_out = np.mean(mean_np)
    std_out = np.mean(std_np)
    print(mean_out, std_out)

    return max_data, min_data, mean_out, std_out


def writeLine(*arg):
    line = ''
    for i in arg:
        line += str(i)
        line += '\t'
    line += '\n'
    with open(path, 'a', encoding='UTF-8') as f:
        f.write(str(line))



# 读取数据集，计算时空数据的mean，std
def st_main():
    txt_path = r'Resource'
    file_list = ['Resource/train.txt', 'Resource/test.txt']
    data_list = []
    for path in file_list:
        with open(path, 'r', encoding='utf-8') as f:
            imgs_info = f.readlines()
            data_list = data_list + list(map(lambda x: x.strip().split('\t'), imgs_info))
    count = len(data_list)

    spatial_mean = []
    spatial_std = []
    date_mean = []
    date_std = []
    time_mean = []
    time_std = []

    spatial_list = []
    time_list = []
    date_list = []

    # 读取数据
    for i in tqdm(range(count)):
        date = data_list[i][2]
        lat = data_list[i][0]
        lon = data_list[i][1]
        time = data_list[i][3]
        ratio = config.ratio
        # 北纬(lat)32°～40°，东经(long)114°～121°
        lat_value = int((40 - float(lat)) / ratio)
        lon_value = int((float(lon) - 114) / ratio)
        spatial_data = spatial_embedding(lat_value, lon_value)
        date_data = date_embedding(date)
        time_data = time_embedding(time)

        spatial_list.append(spatial_data)
        time_list.append(time_data)
        date_list.append(date_data)

    # 均值计算
    spatial_np = np.array(spatial_list)
    time_np = np.array(time_list)
    date_np = np.array(date_list)

    spatial_mean_out = np.mean(spatial_np)
    spatial_std_out = np.std(spatial_np)
    time_mean_out = np.mean(time_np)
    time_std_out = np.std(time_np)
    date_mean_out = np.mean(date_np)
    date_std_out = np.std(date_np)


    # 数据读写
    writeLine('spatial',  1,0,spatial_mean_out, spatial_std_out)
    writeLine('date', 1, 0, date_mean_out, date_std_out)
    writeLine('time',  1,0,time_mean_out, time_std_out)


if __name__ == '__main__':

    st_main()
