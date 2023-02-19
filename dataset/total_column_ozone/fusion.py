# mosica 两张图像
import logging
import os, gdal, glob
import numpy as np
import shutil

from config.log import getLogger

logger = getLogger();


def fusion(output_floder, input1, input2, output):
    # output_floder 输出路径
    # input1,2 两个输入
    # output 输出名字

    os.chdir(output_floder)  # 改变文件夹路径
    # 注册gdal(required)
    gdal.AllRegister()

    # 读入第一幅图像
    ds1 = gdal.Open(input1)
    band1 = ds1.GetRasterBand(1)
    # print(band1.DataType)
    rows1 = ds1.RasterYSize
    cols1 = ds1.RasterXSize

    # 获取图像角点坐标
    transform1 = ds1.GetGeoTransform()
    # print(transform1)
    minX1 = transform1[0]
    maxY1 = transform1[3]
    pixelWidth1 = transform1[1]
    pixelHeight1 = transform1[5]  # 是负值（important）
    maxX1 = minX1 + (cols1 * pixelWidth1)
    minY1 = maxY1 + (rows1 * pixelHeight1)

    # 读入第二幅图像
    ds2 = gdal.Open(input2)
    band2 = ds2.GetRasterBand(1)
    rows2 = ds2.RasterYSize
    cols2 = ds2.RasterXSize

    # 获取图像角点坐标
    transform2 = ds2.GetGeoTransform()
    minX2 = transform2[0]
    maxY2 = transform2[3]
    pixelWidth2 = transform2[1]
    pixelHeight2 = transform2[5]
    maxX2 = minX2 + (cols2 * pixelWidth2)
    minY2 = maxY2 + (rows2 * pixelHeight2)

    # 获取输出图像坐标
    minX = min(minX1, minX2)
    maxX = max(maxX1, maxX2)
    minY = min(minY1, minY2)
    maxY = max(maxY1, maxY2)

    # 获取输出图像的行与列
    cols = int((maxX - minX) / pixelWidth1)
    rows = int((maxY - minY) / abs(pixelHeight1))

    # 计算图1左上角的偏移值（在输出图像中）
    xOffset1 = int((minX1 - minX) / pixelWidth1)
    yOffset1 = int((maxY1 - maxY) / pixelHeight1)

    # 计算图2左上角的偏移值（在输出图像中）
    xOffset2 = int((minX2 - minX) / pixelWidth1)
    yOffset2 = int((maxY2 - maxY) / pixelHeight1)

    # 创建一个输出图像
    driver = ds1.GetDriver()
    dsOut = driver.Create(output, cols, rows, 1, band1.DataType)  # 1是bands，默认
    bandOut = dsOut.GetRasterBand(1)

    # 读图1的数据并将其写到输出图像中
    data1 = band1.ReadAsArray(0, 0, cols1, rows1)
    # bandOut.WriteArray(data1, xOffset1, yOffset1)

    # 读图2的数据并将其写到输出图像中
    data2 = band2.ReadAsArray(0, 0, cols2, rows2)
    # bandOut.WriteArray(data2, xOffset2, yOffset2)

    '''对重叠部分计算最大值'''
    data = np.zeros([rows, cols], dtype=np.float32)
    data1[np.isnan(data1)] = 0
    data2[np.isnan(data2)] = 0

    # np.maximum(data, data2, out=data)
    data = reshape_max(data1, data)
    data = reshape_max(data2, data)

    bandOut.WriteArray(data, 0, 0)

    ''' 写图像步骤'''
    # 统计数据
    bandOut.FlushCache()  # 刷新磁盘
    stats = bandOut.GetStatistics(0, 1)  # 第一个参数是1的话，是基于金字塔统计，第二个
    # 第二个参数是1的话：整幅图像重度，不需要统计
    # 设置输出图像的几何信息和投影信息
    geotransform = [minX, pixelWidth1, 0, maxY, 0, pixelHeight1]
    dsOut.SetGeoTransform(geotransform)
    dsOut.SetProjection(ds1.GetProjection())

    # 建立输出图像的金字塔
    gdal.SetConfigOption('HFA_USE_RRD', 'YES')
    dsOut.BuildOverviews(overviewlist=[2, 4, 8, 16])  # 4层


def reshape_max(data1, data):
    # print(data1.shape)
    # print(data.shape)

    for i, value in np.ndenumerate(data1):
        x = i[0]
        y = i[1]
        if data1[x][y] > data[x][y]:
            data[x][y] = data1[x][y]

    return data


'''格式化数组'''


def arrFormat(data):
    data[np.isnan(data)] = 0


def main(input_floder, output_floder):
    logger.info("路径处理")
    # 路径拼接
    search_criteria = "*.tif"
    q = os.path.join(input_floder, search_criteria)
    print(q)

    # 获取输入路径
    #  O3_20200101T005246_ozone_total_vertical_column.tif
    input_files = glob.glob(q)
    output_files = []

    for i in input_files:
        f_path, f_name = os.path.split(i)
        filename, txt = os.path.splitext(f_name)
        var_name_short = filename[0:11].replace('_', '')
        mark = 0
        for out in output_files:
            if (out["outpath"] == var_name_short):
                mark = 1
                out["inputs"].append(i)
        if (mark == 0):
            out = {"outpath": var_name_short,
                   "inputs": [i]}
            output_files.append(out)

    logger.info("输出数据个数:" + str(len(output_files)))

    logger.info("开始拼接数据")
    for out in output_files:
        count = 0
        output = out["outpath"]
        inputs = out["inputs"]

        inputLen = len(inputs)
        logger.info("开始融合" + str(output) + ".tif，待融合图片{n}个".format(n=inputLen))
        if (inputLen <= 1):
            continue
        temps = []
        while (count < inputLen - 1):
            logger.info("融合" + str(output) + "第{n}次".format(n=count + 1))
            tempout = output + "temp" + str(count) + ".tif"

            if (count == 0):
                input1 = inputs[0]
                input2 = inputs[1]
            else:
                input1 = temps[-1]
                input2 = inputs[count + 1]
            fusion(output_floder=output_floder, input1=input1, input2=input2, output=tempout)
            temps.append(tempout)
            count += 1

        shutil.copy(temps[-1], output + ".tif")
        for i in temps:
            if os.path.isfile(i):
                try:
                    os.remove(i)  # 这个可以删除单个文件，不能删除文件夹
                except BaseException as e:
                    print(e)

        logger.info("融合" + str(output) + ".tif 结束")


if __name__ == '__main__':
    fusion(output_floder=r'D:\work\python\data\tif\TROPOMI\test\fusion',
           input1=r'D:\work\python\data\tif\TROPOMI\test\O3_20200713T053159_ozone_total_vertical_column.tif',
           input2=r'D:\work\python\data\tif\TROPOMI\test\O3_20200713T035030_ozone_total_vertical_column.tif',
           output=r'test.tif')
    # main(input_floder=r'D:\work\python\data\tif\TROPOMI\test', output_floder=r'D:\work\python\data\tif\TROPOMI\test\fusion')
