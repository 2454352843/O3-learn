# -*- coding: utf-8 -*-

import sys
import os
import glob
import numpy as np
import csv
from osgeo import gdal, ogr, osr
from osgeo import gdalconst
import Interpolation


def write_gdal_tif(dataarr, outtif, npDataType, Proj, Transform):
    if npDataType == np.float32:

        gdalDataType = gdal.GDT_Float32

    elif npDataType == np.int16:

        gdalDataType = gdal.GDT_Int16

    elif npDataType == np.uint8:

        gdalDataType = gdal.GDT_Byte

    gtiff_driver1 = gdal.GetDriverByName('GTiff')
    out_ds1 = gtiff_driver1.Create(outtif, dataarr.shape[1], dataarr.shape[0], 1, gdalDataType)
    out_ds1.SetProjection(Proj)
    out_ds1.SetGeoTransform(Transform)
    out_band1 = out_ds1.GetRasterBand(1)
    out_band1.WriteArray(dataarr)
    out_band1.FlushCache()

    del out_ds1


def gettiflist(inputpath):
    tiffiles = []
    for i in range(31):
        i = i + 1
        if i < 10:
            i = '0' + str(i)

        str1 = '2022_05_' + str(i)

        path = inputpath + str1 + os.path.sep
        tiffiles1 = glob.glob(path + "*.tif")
        tiffiles = tiffiles + tiffiles1

    print('list长度: ', len(tiffiles))
    return tiffiles


def resample(list, outpath):
    # 重采样后的分辨率
    gresnew = 0.01

    tiffiles = list

    for i in range(len(tiffiles)):
        tifile = tiffiles[i]

        outdir = outpath + os.path.sep + os.path.sep
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        outtiffile = outdir + os.path.basename(tifile)[:-4] + "_" + "_temp.tif"
        outtif = outdir + os.path.basename(tifile)[:-4] + "_" + ".tif"

        if (os.path.exists(outtif)):
            print(f"{outtif}  exist")
            os.remove(outtif)

        print(f'开始重采样: {tifile}')
        ds = gdal.Open(tifile)
        rows = ds.RasterYSize  # 行数
        cols = ds.RasterXSize  # 列数
        bands = ds.RasterCount
        Proj = ds.GetProjection()
        Transform = ds.GetGeoTransform()
        del ds

        maxLatmain = Transform[3]
        minLatmain = Transform[3] + rows * Transform[5]
        minLonmain = Transform[0]
        maxLonmain = Transform[0] + cols * Transform[1]

        # 投影后的经纬度
        lata = np.arange(maxLatmain, minLatmain, -1.0 * gresnew)
        lona = np.arange(minLonmain, maxLonmain, gresnew)
        match_lon, match_lat = np.meshgrid(lona, lata)
        xsize = match_lon.shape[1]
        ysize = match_lon.shape[0]

        Interpolation.cubicDeal(tifile, outtiffile, xsize, ysize)

        ds1 = gdal.Open(outtiffile)
        Proj1 = ds1.GetProjection()
        Transform1 = ds1.GetGeoTransform()
        Bandarr = ds1.GetRasterBand(1).ReadAsArray()
        Bandarr[Bandarr<=0] = np.nan
        del ds1

        Transforma = [Transform1[0], gresnew, Transform1[2], Transform1[3], Transform1[4], -gresnew]

        npDataType = np.float32

        write_gdal_tif(Bandarr, outtif, npDataType, Proj1, Transforma)

        os.remove(outtiffile)


def main():
    inputpath = r'F:\data\xyz-O3\S5P\workspace\workspace-20230301-230401\7missingCompleting'
    outputpath = r"F:\data\xyz-O3\S5P\workspace\workspace-20230301-230401\8resample"

    list = glob.glob(inputpath + os.path.sep + '*.tif')

    # 调用裁剪方法
    resample(list, outputpath)


if __name__ == '__main__':
    main()
