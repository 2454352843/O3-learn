# -*- coding: UTF-8 -*-
import os
import glob
import arcpy
from arcpy.sa import *

'''
功能：
    缺失补全
'''

arcpy.CheckOutExtension("ImageAnalyst")  # 检查许可
arcpy.CheckOutExtension("spatial")

# 工作空间
nc_folder = r'E:\data\1. S5P_OFFL_L2_O3\workspace-20220930-20230301'
# tif文件夹
input_folder = os.path.join(nc_folder, '6zhuanhuan')
# grid output_folder 计算后文件夹
output_folder = os.path.join(nc_folder, '7missingCompleting')

# 利用glob包，将inws下的所有tif文件读存放到rasters中
rasters = glob.glob(os.path.join(input_folder, "*.tif"))

# 循环rasters中的所有影像，进行“求平均值”操作
for ras in rasters:
    print ras
    # Con(IsNull(“raster”), FocalStatistics(“raster”, NbrRectangle(5,5, “CELL”), “MEAN”), “raster”)
    outRas2 = FocalStatistics(ras, NbrRectangle(5, 5, "CELL"), "MEAN")
    outras = Con(IsNull(ras), outRas2, ras)

    path1, filename = os.path.split(ras)
    output = output_folder + os.path.sep + filename
    outras.save(output)  # 保存

print("All project is OK！")
