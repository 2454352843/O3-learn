import signal

import multitasking
from osgeo import gdal, gdalconst
import numpy as np
import os
from tqdm import tqdm
from Resource import config
'''
计算最大值，最小值，归一化，标准差，均值
计算的太慢了，需要多线程调用
异步计算tropomi之后的数据
'''
# 按快捷键 ctrl + c 终止已开启的全部线程
signal.signal(signal.SIGINT, multitasking.killall)
multitasking.set_max_threads(4)  # 最大线程数为cpu核数*2

path = r'Resource/math2.txt'
rootdata = config.base_path

tif_list = ['SILAM']

GEOS = ['PS','T2M','TROPCOL_O3','U2M','V2M','ZPBL']

LandCover = ['DEM','NDVI','POP','pri_sec.tif']
# LandCover = ['tertiary']


img_list = ['PS','T2M','TROPCOL_O3','U2M','V2M','ZPBL','SILAM','Tropomi','DEM','NDVI','POP','pri_sec']

# rasterlist = []



def normalization(data,max_data,min_data):

    _range = max_data - min_data
    return (data - min_data) / _range



def math_count(inputFilePath,label = ''):
    Files = []
    print(f'input:{inputFilePath},label = {label}')
    meanlist = []
    stdlist = []


    # 1. 数据读取

    max_data = -100
    min_data = 10000000
    for root, dirs, files in os.walk(inputFilePath):
        files = files
        for file in files:
            if os.path.splitext(file)[-1] == '.tif' and label in file:  # 查找.tif文件
                sourcefile = os.path.join(root, file)  # 拼路径
                Files.append(sourcefile)
    # print(Files)

    # 2. 归一化处理
    for file1 in (Files):

        dataset = gdal.Open(file1, gdalconst.GA_ReadOnly)
        # dataset_geo_trans = dataset.GetGeoTransform()
        # col = dataset.RasterXSize
        # row = dataset.RasterYSize
        raster_data1 = dataset.GetRasterBand(1).ReadAsArray()  # 以数组的形式读取栅格点数据
        raster_data1 = raster_data1[raster_data1>-1000] # 排除异常值
        if (raster_data1.size == 0):
            print(f'{file1} is null')
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
        raster_data1 = normalization(raster_data1,max_data,min_data)

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

    return max_data,min_data,mean_out,std_out


def writeLine(*arg):
    line = ''
    for i in arg:
        line += str(i)
        line += '\t'
    line += '\n'
    with open(path, 'a', encoding='UTF-8') as f:

        f.write(str(line))

@multitasking.task
def main_tif(i):
    max, min, mean, std = math_count(rootdata + os.path.sep + i)
    print(i, max, min, mean, std)
    writeLine(i, max, min, mean, std)

@multitasking.task
def main_GEOS(i):
    max, min, mean, std = math_count(rootdata + os.path.sep + 'GEOS', i)
    print(i, max, min, mean, std)
    writeLine(i, max, min, mean, std)

def main():
    # for i in LandCover:
    #     max, min, mean, std = math_count(rootdata + os.path.sep + 'LandCover', i)
    #     print(i, max, min, mean, std)
    #     writeLine(i, max, min, mean, std)


    for i in tif_list:
        main_tif(i)


    for i in GEOS:
        main_GEOS(i)
    multitasking.wait_for_tasks()





if __name__ == '__main__':
  main()




