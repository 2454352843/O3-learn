from osgeo import gdal, gdalconst
import numpy as np
import os
from tqdm import tqdm

def normalization(data):

    _range = max_data - min_data

    return (data - min_data) / _range

inputFilePath= r"E:\data\5-mouth-dataset\GEOS-test"
Files = []
meanlist=[]
stdlist=[]
rasterlist=[]
max_data = 0
min_data = 1000000


if __name__ == '__main__':

    #1. 数据读取
    for root, dirs, files in os.walk(inputFilePath):
        files=files
        for file in files:
            if os.path.splitext(file)[1] == '.tif':  # 查找.tif文件
                sourcefile = os.path.join(root, file)  # 拼路径
                Files.append(sourcefile)
    #print(Files)

    #2. 归一化处理
    for file1 in tqdm(Files):
        dataset = gdal.Open(file1,gdalconst.GA_ReadOnly)
        dataset_geo_trans = dataset.GetGeoTransform()
        col = dataset.RasterXSize
        row = dataset.RasterYSize
        raster_data1 = dataset.GetRasterBand(1).ReadAsArray()  # 以数组的形式读取栅格点数据
        max_data = np.max(raster_data1) if np.max(raster_data1) > max_data else max_data
        min_data = np.min(raster_data1) if np.min(raster_data1) < min_data else min_data

    #3. 计算标准差，均值
    for file1 in tqdm(Files):
        dataset = gdal.Open(file1, gdalconst.GA_ReadOnly)
        dataset_geo_trans = dataset.GetGeoTransform()
        col = dataset.RasterXSize
        row = dataset.RasterYSize
        raster_data1 = dataset.GetRasterBand(1).ReadAsArray()
        raster_data1 = normalization(raster_data1)
        meandata = np.mean(raster_data1)
        stddata = np.std(raster_data1)
        meanlist.append(meandata)
        stdlist.append(stddata)

    print(f"max value : {max_data}")
    print(f"min value : {min_data}")
    mean_np = np.array(meanlist)
    std_np = np.array(stdlist)

    mean_out = np.mean(mean_np)
    std_out = np.mean(std_np)
    print(mean_out,std_out)
