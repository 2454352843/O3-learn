# -*- coding: utf-8 -*-
from datetime import timedelta, date

import arcpy, os
import glob
from arcpy.sa import *

'''
裁剪 workspace下和其子目录下的所有tif
根据指定的tif，裁剪其余tif
'''
arcpy.CheckOutExtension("Spatial")

# .nc files path

# tif文件夹
worksapce = r'F:\data\xyz-O3\GEOS-CF\workspace\weather\2tif'
output_floder = r'F:\data\xyz-O3\GEOS-CF\workspace\weather\3clip'

# .shp file path
mask_shp = r"E:\data\5-mouth-dataset\LandCover\2022_05_09\DEM.tif"


def clipRaster(work_folder, mosaic_list):
    arcpy.env.workspace = output_floder

    num = 0
    for in_raster in mosaic_list:
        if ('DEM' in in_raster):
            continue
        # Execute ExtractByMask

        base_name = os.path.basename(in_raster)
        date = in_raster.split(os.path.sep)[-2]
        outdir = output_floder + os.path.sep + date
        out_name = outdir+ os.path.sep + base_name
        if not os.path.exists(outdir):
            os.makedirs(outdir)

        outExtractByMask = ExtractByMask(in_raster, mask_shp)
        try:
            # os.remove(in_raster)
            outExtractByMask.save(out_name)

        except Exception:

            print Exception
            print in_raster + ' error'

        num += 1
        print(in_raster + ' success')
    print('Numbers: ', num)
    print('-' * 50)


def main():
    for root, dirs, files in os.walk(worksapce):

        print root
        list3 = [n for n in filter(lambda x: 'tif' in x[-3:], files)]
        tifs = [root + os.path.sep + tif for tif in list3]

        if len(tifs) > 0:
            # 调用裁剪方法
            clipRaster(root, tifs)


if __name__ == "__main__":
    main()
