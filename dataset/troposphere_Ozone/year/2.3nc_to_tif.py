import logging
import os
import time

import netCDF4 as nc
import numpy as np
from osgeo import gdal, osr, ogr
import glob
# 导入用于多线程操作的库
# 这样子仅需要在自定义的函数前面使用装饰器即可将函数开启新的线程
import multitasking
import signal

# 按快捷键 ctrl + c 终止已开启的全部线程
from dataset.troposphere_Ozone.year import NC_Util

signal.signal(signal.SIGINT, multitasking.killall)
multitasking.set_max_threads(4)  # 最大线程数为4
logger = logging.getLogger()

def converSearchTable(lats, lons, PRES, MAXLAT, MINLON):
    """
    转换查找表
    """

    lats = np.asarray(lats)
    lons = np.asarray(lons)

    lines = (MAXLAT - lats) / PRES
    lines = lines.astype(np.int32)

    cols = (lons - MINLON) / PRES
    cols = cols.astype(np.int32)

    return lines, cols


# @multitasking.task
def nc2tif(data, Output_folder):
    value_threshold = 0.75  # 质量控制qu_value

    startime = time.time()
    ncdata = NC_Util.NCopen(data)

    # print(((ncdata.groups)["PRODUCT"]).variables.keys())

    Lat_data = NC_Util.ReadNcDataset3(ncdata, "latitude")
    Lon_data = NC_Util.ReadNcDataset3(ncdata, "longitude")
    O3arr = NC_Util.ReadNcDataset3(ncdata, "ozone_tropospheric_column")
    value = NC_Util.ReadNcDataset3(ncdata, "qa_value")

    # 影像的左上角&右下角坐标
    Lonmin, Latmax, Lonmax, Latmin = [Lon_data.min(), Lat_data.max(), Lon_data.max(), Lat_data.min()]
    # Lonmin, Latmax, Lonmax, Latmin

    # 分辨率计算
    Num_lat = len(Lat_data)
    Num_lon = len(Lon_data)
    Lat_res = (Latmax - Latmin) / (float(Num_lat) - 1)
    Lon_res = (Lonmax - Lonmin) / (float(Num_lon) - 1)
    # print(Num_lat, Num_lon)
    # print(Lat_res, Lon_res)

    LatarrNew = Lat_data[0]
    LonarrNew = Lon_data[0]
    O3arrNew = O3arr[0]
    qa_value = value[0]

    O3arrNew[qa_value <= value_threshold] = 0
    pre_arr = O3arrNew.reshape(O3arr.shape)

    # i=0,1,2,3,4,5,6,7,8,9,...
    # 创建tif文件
    driver = gdal.GetDriverByName('GTiff')
    out_tif_name = Output_folder + (os.path.basename(data))[:-3] + ".tif"
    out_tif = driver.Create(out_tif_name, Num_lon, Num_lat, 1, gdal.GDT_Int16)

    # 设置影像的显示范围
    # Lat_re前需要添加负号
    geotransform = (Lonmin, Lon_res, 0.0, Latmax, 0.0, -Lat_res)
    out_tif.SetGeoTransform(geotransform)

    # 定义投影
    prj = osr.SpatialReference()
    prj.ImportFromEPSG(4326)
    out_tif.SetProjection(prj.ExportToWkt())
    # 数据导出
    out_tif.GetRasterBand(1).WriteArray(pre_arr)  # 将数据写入内存
    out_tif.FlushCache()  # 将数据写入到硬盘
    out_tif = None  # 关闭tif文件

    print('{data}用时{i}s'.format(data = data,i=(time.time() - startime)))


# 检验函数 检验列表里的文件是否能够打开，是否重复
def jianyan(list):
    list1 = list
    for i in list:
        try:
            pre_data = nc.Dataset(i)

        except:
            print(f"{i}打不开")
            list1.remove(i)

        else:
            pre_data.close()
        for j in list:
            if(j.split('.')[0]== i.split('.')[0]) and (i != j):

                if  ("nc4" in i):
                    print(f"{i} he {j} 文件名一致，删除{i}")
                    list1.remove(i)



    return list1


def main():
    Input_folder = r'F:\data\xyz-O3\SILAM\workspace\1nc'
    Output_folder = r'F:\data\xyz-O3\SILAM\workspace\2tif'
    start_time = time.time()
    # 读取所有数据
    data_list_nc = glob.glob(os.path.join(Input_folder, '*.nc'))
    data_list_nc.sort()

    data_list_nc4 = glob.glob(os.path.join(Input_folder, '*.nc4'))
    data_list_nc4.sort()

    data_list = data_list_nc4 + data_list_nc
    data_list = jianyan(data_list)

    print('共有{i}条数据'.format(i =len(data_list)))

    for i in range(len(data_list)):
        data = data_list[i]
        logger.info(f"开始转换{data} ")
        nc2tif(data, Output_folder)
    multitasking.wait_for_tasks()
    print('总用时{i}s'.format(i=(time.time() - start_time)))



# data = r'E:\data\3. SILAM\workspace\1nc\SILAM-AQ-china_v5_5_1_2022101300_001.nc4'
# Output_folder = r'E:\data\3. SILAM\workspace\2te'
# nc2tif(data, Output_folder)
if __name__ == '__main__':
    # main()

    a = np.array([[1,2,3],[4,5,6]])
    b = np.array(([1,2,3,4,5,6]))
    print(b)
    print(b.reshape(a.shape))