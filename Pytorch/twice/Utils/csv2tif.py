
#2022.3.10 杨宣1
#2022.5.12 csv文件转tif的 月均值 精度为1
import numpy as np
from osgeo import gdal, osr
from glob import glob
import os
import datetime
import pandas as pd
os.environ['PROJ_LIB'] = r'E:\python\Lib\site-packages\osgeo\data\proj'
def csv2array(filen):
    df = pd.read_csv(filen)
    lat = (np.array((df.loc[:,'lat']).tolist())).reshape(-1,1)
    lon = (np.array((df.loc[:,'lon']).tolist())).reshape(-1,1)
    co2 = (np.array((df.loc[:,'t']).tolist())).reshape(-1,1)

    ns = []
    nl = []
    for line in lon:
        # ns.append(int(line))
        ns.append(float(line))
    ns = sorted(ns)
    unique_data1 = np.unique(ns)
    print('lon的值为')
    print(unique_data1)
    for line in lat:
        # nl.append(int(line))
        nl.append(float(line))
    nl = sorted(nl)
    unique_data2 = np.unique(nl)
    print('lat的值为')
    print(unique_data2)
    xx, yy = [len(unique_data2), len(unique_data1)]
    # outdata = co2.reshape(xx, yy)
    outdata = co2.reshape(xx, yy)  # 横坐标和纵坐标 经纬度个数
    res_lon = abs(unique_data1[1] - unique_data1[0])
    print(res_lon)
    res_lat = abs(unique_data2[1] - unique_data2[0])
    # res_lat = -abs(unique_data2[1] - unique_data2[0])
    print(res_lat)
    latmin = np.min(unique_data2)
    # latmax = np.max(unique_data2)
    lonmin = np.min(unique_data1)
    return outdata, res_lon, res_lat, latmin, lonmin

def writetif(data, outname, geotransform):
    nl, ns = [data.shape[0], data.shape[1]]
    print('ns的值为+')
    print(nl)
    print('ns的值为+')
    print(ns)
    bands = 1
    driver = gdal.GetDriverByName("GTiff")
    out_tif = driver.Create(outname, ns, nl, bands, gdal.GDT_Float32)
    out_tif.SetGeoTransform(geotransform)
    srs = osr.SpatialReference()
    proj_type = 'GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AXIS["Latitude",NORTH],AXIS["Longitude",EAST],AUTHORITY["EPSG","4326"]]'
    out_tif.SetProjection(proj_type)  # 给新建图层赋予投影信息
    out_tif.GetRasterBand(1).WriteArray(data)
    del out_tif


inpath  = 'L:\\xianyu\\01'
outpath = 'L:\\xianyu\\01'


dirs = os.listdir(inpath)  # 获取指定路径下的文件
file_name = []

for x in dirs:  # 循环读取路径下的文件并筛选输出
    if os.path.splitext(x)[1] == '.csv' or os.path.splitext(x)[1] == '.CSV':   # 筛选.HDF文件
        file_name.append(x)
for k in range(len(file_name)):
    filename = inpath+'/'+file_name[k]
    tt = file_name[k]
    outdata,res_lon,res_lat,latmax,lonmin = csv2array(filename)
    geotransform =  (lonmin, res_lon, 0, latmax, 0, res_lat)
    outname = outpath + '/' + tt[0:len(tt)-3] + 'tif'
    writetif(outdata,outname,geotransform)