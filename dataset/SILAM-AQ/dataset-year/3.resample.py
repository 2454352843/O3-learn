# -*- coding: utf-8 -*-

import sys
import os
import glob
import numpy as np
import tqdm
from osgeo import gdal, ogr, osr
from osgeo import gdalconst
import Interpolation

'''
使用数据为自己下载的数据
重采样：目标文件夹内全部tif格式文件均进行重采样处理
'''
def write_gdal_tif(dataarr,outtif,npDataType,Proj,Transform):

    if npDataType == np.float32 :

        gdalDataType = gdal.GDT_Float32

    elif npDataType == np.int16 :

        gdalDataType = gdal.GDT_Int16

    elif npDataType == np.uint8 :

        gdalDataType = gdal.GDT_Byte

    gtiff_driver1=gdal.GetDriverByName('GTiff')
    out_ds1=gtiff_driver1.Create(outtif,dataarr.shape[1],dataarr.shape[0],1,gdalDataType)
    out_ds1.SetProjection(Proj)
    out_ds1.SetGeoTransform(Transform)
    out_band1=out_ds1.GetRasterBand(1)
    out_band1.WriteArray(dataarr)
    out_band1.FlushCache()

    del out_ds1

def gettiflist(inputpath):
    tiffiles = []

    tiffiles = glob.glob(inputpath + "*.tif")

    print('list长度: ',len(tiffiles))
    return  tiffiles



def main():

    inputpath = r"F:\data\xyz-O3\SILAM\workspace\2tif" + os.path.sep
    outputpath = r"F:\data\xyz-O3\SILAM\workspace\3reshape" + os.path.sep

    # 重采样后的分辨率
    gresnew = 0.01


    tiffiles = gettiflist(inputpath)

    for i in (range(len(tiffiles))):

        tifile = tiffiles[i]


        outtiffile = outputpath + os.path.basename(tifile)[:-4] + "_temp.tif"
        outtif = outputpath + os.path.basename(tifile)[:-4] + ".tif"

        if  (os.path.exists(outtif)):
            print(f"{outtif}  exist")
            os.remove(outtif)


        print(f'开始重采样: {tifile}')
        ds=gdal.Open(tifile)
        rows = ds.RasterYSize  #行数
        cols = ds.RasterXSize  #列数
        bands = ds.RasterCount
        Proj = ds.GetProjection()
        Transform = ds.GetGeoTransform()
        del ds

        maxLatmain = Transform[3]
        minLatmain = Transform[3] + rows*Transform[5]
        minLonmain = Transform[0]
        maxLonmain = Transform[0] + cols*Transform[1]

        # 投影后的经纬度
        lata = np.arange(maxLatmain,minLatmain,-1.0*gresnew)
        lona = np.arange(minLonmain,maxLonmain,gresnew)
        match_lon,match_lat = np.meshgrid(lona,lata)
        xsize = match_lon.shape[1]
        ysize = match_lon.shape[0]

        Interpolation.cubicDeal(tifile,outtiffile,xsize,ysize)

        ds1=gdal.Open(outtiffile)
        Proj1 = ds1.GetProjection()
        Transform1 = ds1.GetGeoTransform()
        Bandarr = ds1.GetRasterBand(1).ReadAsArray()
        del ds1

        Transforma = [Transform1[0],gresnew,Transform1[2],Transform1[3],Transform1[4],-gresnew]


        npDataType = np.uint8

        write_gdal_tif(Bandarr,outtif,npDataType,Proj1,Transforma)

        os.remove(outtiffile)

if __name__ == '__main__':
    main()