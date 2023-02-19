# -*- coding: utf-8 -*-

import sys
import os
import glob
from osgeo import gdal,ogr,osr
from scipy import ndimage as nd
import datetime
import time
import numpy as np
import pandas as pd

def converSearchTable(lats,lons,PRES,MAXLAT,MINLON):
    """
    转换查找表
    """

    lats = np.asarray(lats)
    lons = np.asarray(lons)

    lines = (MAXLAT - lats) / PRES
    lines = lines.astype(np.int32)

    cols = (lons - MINLON) / PRES 
    cols = cols.astype(np.int32)


    return lines,cols

def write_gdal_tif(dataarr,outtif,npDataType,Proj,Transform):

    if npDataType == np.float32 :

        gdalDataType = gdal.GDT_Float32

    elif npDataType == np.float64 :

        gdalDataType = gdal.GDT_Float64

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

if __name__ == "__main__":

    inputpath = r"E:\data\6. site\5yuedataset\xlsx" + os.path.sep
    outputpath = r"E:\data\6. site\5yuedataset\1totif" + os.path.sep

    resolution = 0.01

    hourTlist = ["00:00:00.0000000","01:00:00.0000000","02:00:00.0000000","03:00:00.0000000","04:00:00.0000000"
    ,"05:00:00.0000000","06:00:00.0000000","07:00:00.0000000","08:00:00.0000000","09:00:00.0000000"
    ,"10:00:00.0000000","11:00:00.0000000","12:00:00.0000000","13:00:00.0000000","14:00:00.0000000"
    ,"15:00:00.0000000","16:00:00.0000000","17:00:00.0000000","18:00:00.0000000","19:00:00.0000000"
    ,"20:00:00.0000000","21:00:00.0000000","22:00:00.0000000","23:00:00.0000000"]

    xlsxfiles = glob.glob(inputpath + "*.xlsx")

    for i in range(len(xlsxfiles)):

        xlsxfile = xlsxfiles[i]
        print(xlsxfile.split(os.path.sep))
        df=pd.read_excel(xlsxfile)

        Latlist = df.values[:,1]
        Lonlist = df.values[:,2]
        O3list = df.values[:,6]

        Timelist = df.values[:,5]

        for j in range(len(hourTlist)):

            hourT = hourTlist[j]

            outtif = outputpath + os.path.basename(xlsxfile)[:-5].replace('-','_') + "_" + hourT[:2] + ".tif"
            print(outtif.split(os.path.sep)[-1])
            mask = Timelist == hourT

            LatlistNew = Latlist[mask]
            LonlistNew = Lonlist[mask]
            O3listNew = O3list[mask]
            if (len(O3listNew)<1):
                continue
            
            minLat = min(LatlistNew)
            maxLat = max(LatlistNew)
            minLon = min(LonlistNew)
            maxLon = max(LonlistNew)

            lines,cols = converSearchTable(LatlistNew,LonlistNew,resolution,maxLat,minLon)

            height_new = int((maxLat - minLat) / resolution)
            width_new = int((maxLon - minLon) / resolution)

            img_new1 = np.zeros((height_new,width_new),dtype = np.float32)
            # print ("height_new, width_new = ",height_new, width_new)

            img_new1[:,:][lines-1,cols-1] = O3listNew

            # 定义空间参考系
            im_geotrans=[minLon,resolution,0,maxLat,0,-resolution]
            srs=osr.SpatialReference()
            srs.SetWellKnownGeogCS('WGS84')
            im_proj =srs.ExportToWkt()

            npDataType = np.float32
            write_gdal_tif(img_new1,outtif,npDataType,im_proj,im_geotrans)


