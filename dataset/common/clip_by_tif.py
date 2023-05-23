# -*- coding: utf-8 -*-
from datetime import timedelta, date

import arcpy, os
import glob
from arcpy.sa import *

'''
裁剪 5月份的数据
根据指定的tif，裁剪其余tif
'''
arcpy.CheckOutExtension("Spatial")

# .nc files path

# tif文件夹
worksapce = r'I:\data\dataset\LandCover\pop'
output_ = r'I:\data\dataset\LandCover\pop'
# .shp file path
mask_shp = r"I:\data\xyz-O3\LandCover\DEM.tif"
tif_list = ['GEOS',  'SILAM', 'Tropomi']

def clipRaster(work_folder, mosaic_list):
    arcpy.env.workspace = work_folder

    num = 0
    for in_raster in mosaic_list:
        if('DEM' in in_raster):
            continue
        # Execute ExtractByMask
        basepath,basename = os.path.split(in_raster)
        date = basepath.split(os.path.sep)[-1]
        # output_folder = output_ + os.path.sep + date
        output_folder = output_
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        clip_name = output_folder + os.path.sep+ basename[:-4].split(os.path.sep)[-1] + '.tif'

        outExtractByMask = ExtractByMask(in_raster, mask_shp)
        try:
            os.remove(in_raster)
            outExtractByMask.save(clip_name)

        except Exception:

            print Exception
            print in_raster+' error'

        num += 1
        print(in_raster+' success')
    print('Numbers: ', num)
    print('-' * 50)


def main():


    for root, dirs, files in os.walk(worksapce):

        list3 = [n for n in filter(lambda x: 'tif' in x[-3:],files )]
        tifs = [root+ os.path.sep + tif for  tif in list3]

        if len(tifs)>0:


            # 调用裁剪方法
            clipRaster(root, tifs)



if __name__ == "__main__":
    main()


