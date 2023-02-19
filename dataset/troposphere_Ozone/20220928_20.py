# -*- coding: utf-8 -*-

import os
import time
import glob
import numpy as np
from osgeo import gdal,osr
from scipy import ndimage as nd

import NC_Util

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

def write_gdal_tifs(dataarr,outtif,npDataType,Proj,Transform,bands):

    if npDataType == np.float32 :

        gdalDataType = gdal.GDT_Float32

    elif npDataType == np.int16 :

        gdalDataType = gdal.GDT_Int16
    
    elif npDataType == np.int32 :

        gdalDataType = gdal.GDT_Int32

    elif npDataType == np.uint8 :

        gdalDataType = gdal.GDT_Byte

    gtiff_driver1=gdal.GetDriverByName('GTiff')
    out_ds1=gtiff_driver1.Create(outtif,dataarr.shape[2],dataarr.shape[1],bands,gdalDataType)
    out_ds1.SetProjection(Proj)
    out_ds1.SetGeoTransform(Transform)

    for i in range(bands):

        out_band1=out_ds1.GetRasterBand(i+1)
        out_band1.WriteArray(dataarr[i])

    out_band1.FlushCache()

    del out_ds1


def fill(data, invalid=None):
    if invalid is None:
        invalid1 = np.isnan(data)
    else:
        invalid1 = data == invalid

    distances, indices = nd.distance_transform_edt(invalid1, return_distances=True, return_indices=True)
    data = data[tuple(indices)]
    # data[distances > 10] = invalid  # 距离阈值设置为10，可以修改
    data[distances > 3] = invalid   

    return data


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



if __name__ == "__main__":

    a=time.time()

    inputpath = "D:/PersonWork/20220927/NEW/NCdata/"
    outputpath = "D:/PersonWork/20220927/NEW/tifdata/"

    nctifs = glob.glob(inputpath + "*.nc")

    for i in range(len(nctifs)):

        nctif = nctifs[i]

        outtif = outputpath + (os.path.basename(nctif))[:-3] + ".tif"

        print(nctif)

        ncdata = NC_Util.NCopen(nctif)

        # print(((ncdata.groups)["PRODUCT"]).variables.keys())

        Latarr = NC_Util.ReadNcDataset3(ncdata, "latitude")
        Lonarr = NC_Util.ReadNcDataset3(ncdata, "longitude")
        O3arr = NC_Util.ReadNcDataset3(ncdata, "ozone_tropospheric_column")

        LatarrNew = Latarr[0]
        LonarrNew = Lonarr[0]
        O3arrNew = O3arr[0]

        minLon = np.min(LonarrNew)
        maxLon = np.max(LonarrNew)

        minLat = np.min(LatarrNew)
        maxLat = np.max(LatarrNew)

        mask = (LatarrNew >= minLat) & (LatarrNew <= maxLat) & (LonarrNew >= minLon) & (LonarrNew <= maxLon) 
        lats = LatarrNew[mask]
        lons = LonarrNew[mask]

        resolution = 0.3

        O3arrNew[O3arrNew > 10000] = 0

        lines,cols = converSearchTable(lats,lons,resolution,maxLat,minLon)

        height_new = int((maxLat - minLat) / resolution)
        width_new = int((maxLon - minLon) / resolution)
        img_new = np.zeros((height_new,width_new),dtype = np.float64)

        print ("height_new, width_new = ",height_new, width_new)
        img_new[:,:][lines-1,cols-1] = O3arrNew[mask]

        img_new1 = np.zeros((height_new,width_new),dtype = np.float64)
        img_new1 = fill(img_new, invalid=0)

        im_geotrans=[minLon,resolution,0,maxLat,0,-resolution]
        srs=osr.SpatialReference()
        srs.SetWellKnownGeogCS('WGS84')
        im_proj =srs.ExportToWkt()
        npDataType = np.float64 

        write_gdal_tif(img_new1,outtif,npDataType,im_proj,im_geotrans)
        
        NC_Util.NCclose(ncdata)

