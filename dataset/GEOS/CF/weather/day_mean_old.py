# -*- coding: UTF-8 -*-
import arcpy, sys, os, glob
from arcpy.sa import *
import numpy

'''
批量计算平均栅格（一级目录）：
    对输入文件夹下的数据 计算平均值，结果存放于输出文件夹

    需要修改：
        inws：输入路径（必选）
        outws：输出路径（必选）
        nameT：这里要进行下规范化，文件名的易读性（可选）
'''

arcpy.CheckOutExtension('Spatial')

# 输入路径  应该注意，中文路径，会导致读不出文件
inws = r"E:\data\workspace\5mouthdata\geos-cf"

# 输出路径
outws = r"E:\data\workspace\testdaymean\output"


def day_mean():
    # 利用glob包，将inws下的所有tif文件读存放到rasters中
    rasters = glob.glob(os.path.join(inws, "*.tif"))

    r = Raster(rasters[0])  # 打开栅格
    array = arcpy.RasterToNumPyArray(r)  # 转成Numpy方便对每个像元进行处理
    rowNum, colNum = array.shape  # 波段、行数、列数

    sum = numpy.zeros(shape=array.shape)    # 存储累加值
    count = numpy.zeros(shape=array.shape)  # 存储 有效像元计数器
    Average = numpy.zeros(shape=array.shape)    # 存储 平均值

    # 循环rasters中的所有影像，进行按掩模提取操作
    for ras in rasters:
        rmm = Raster(ras)  # 打开栅格
        array = arcpy.RasterToNumPyArray(rmm)  # 转成Numpy方便对每个像元进行处理

        # 逐像元计算
        for i in range(0, rowNum):
            for j in range(0, colNum):
                if array[i][j] > 0 :  # 判断有效值
                    sum[i][j] += array[i][j]  # 累加
                    count[i][j] += 1    # 计数器
                    continue

    Average = sum / count   # 平均值计算

    # 保存栅格
    lowerLeft = arcpy.Point(r.extent.XMin, r.extent.YMin)  # 左下角点坐标
    cellWidth = r.meanCellWidth  # 栅格宽度
    cellHeight = r.meanCellHeight

    nameT = os.path.basename(rasters[0])
    outname = os.path.join(outws, nameT)  # 合并输出文件名+输出路径

    arcpy.env.overwriteOutput = True    # 覆盖输出文件夹已有内容
    arcpy.env.outputCoordinateSystem = rasters[0]   # 输出坐标系与输入相同

    AvgRas = arcpy.NumPyArrayToRaster(Average, lowerLeft, cellWidth, cellHeight, r.noDataValue)  # 转换成栅格
    AvgRas.save(outname)  # 保存

    print os.path.basename(rasters[0]) + " ---- 完成"


def main():
    file_list = os.listdir(inws)
    for i in range(len(file_list)):
        print i


if __name__ == '__main__':
    main()