# -*- coding: utf-8 -*-
from datetime import timedelta, date

import arcpy, os
import glob
from arcpy.sa import *
'''
裁剪 5月份的数据
对于老师给的处理完成的数据，进行裁剪，裁剪完放入指定文件夹中，根据天数进行存放
'''
arcpy.CheckOutExtension("Spatial")

# .nc files path

# tif文件夹
worksapce = r'E:\data\3. SILAM\processed'

#  裁剪文件夹
clip_folder = r'E:\data\3. SILAM\5yuedataset\1clip'
# .shp file path
mask_shp = r"D:\work\python\data\china\国界.shp"


def clipRaster(data, time, work_folder, mosaic_list):
    if not os.path.exists(clip_folder):
        os.makedirs(clip_folder)
    arcpy.env.workspace = work_folder
    last_folder = clip_folder + os.path.sep + data
    if not os.path.exists(last_folder):
        os.makedirs(last_folder)

    num = 0
    for in_raster in mosaic_list:
        # Execute ExtractByMask
        arcpy.env.snapRaster = in_raster
        clip_name = in_raster[:-4].split(os.path.sep)[-1] + '_'+time + '.tif'
        prj_clip = last_folder + '\\' + clip_name
        outClip = ExtractByMask(in_raster, mask_shp)
        outClip.save(prj_clip)
        num += 1
        print(clip_name)
    print('Numbers: ', num)
    print('-' * 50)


def main():
    for i in range(31):
        i = i + 1
        if i < 10:
            i = '0' + str(i)

        str1 = '2022_05_' + str(i)
        print str1

        for j in range(24):
            if j < 10:
                j = '0' + str(j)

            work_folder = worksapce + os.path.sep + str1 + os.path.sep + str(j)
            list = glob.glob(work_folder+os.path.sep +'*.tif')

            # 调用裁剪方法
            clipRaster(str1, str(j), work_folder, list)


if __name__ == "__main__":
    main()
