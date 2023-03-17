# 测试验证数据集读取  核心是验证 Gdaltiff()数据读取 是否正确
import os

from random import random, randint

import gdal
import config.log as log
from Dataset import LoadData, Point
from Pytorch.twice.Resource import config

from Pytorch.twice.utils import *
logger = log.getLogger()

mean1, std1, max1, min1 = get_math()
# 删除临时文件
def del_files(dir_path):
    for root, dirs, files in os.walk(dir_path, topdown=False):
        # 第一步：删除文件
        for name in files:
            os.remove(os.path.join(root, name))  # 删除文件


# 从tif根据经纬度读取数据
def get_value_from_xy(file, point):
    dataset = gdal.Open(file)
    x = float(point.lon)
    y = float(point.lat)
    step = 0.015
    minx = x - step
    maxx = x + step
    miny = y - step
    maxy = y + step

    outputSrtm = "./temp" + 'ski23eu84'  # 输出的临时缓存文件
    data = gdal.Translate(outputSrtm, srcDS=dataset, projWin=[minx, maxy, maxx, miny])
    data = data.ReadAsArray()
    data_list = data.flatten()  # 把数据一维展开

    del_files(outputSrtm)
    return data_list


# 判断两个数的大小，相差小于0.1%为true
def examin(x, y):
    max = x if x > y else y
    min = x if y == max else y

    rate = (max - min) / min
    print(f'rate : {rate}')
    if (rate > 0.001):
        return False

    return True


def examine_train():
    # batch_size = config.batch_size
    # batch_size = 128
    arr_list = config.arr_list
    # # 给训练集和测试集分别创建一个数据集加载器
    train_data = LoadData("Resource/train.txt", True)
    # train_dataloader = DataLoader(dataset=train_data, num_workers=4, pin_memory=True, batch_size=batch_size, shuffle=True)
    size = len(train_data.imgs_info)

    # 随机选择100个数据进行测试
    for i in range(100):
        index = randint(0, int(size))
        point = Point(train_data.imgs_info[index])
        data, label = train_data[index]

        # 根据point 验证使用的图片
        date = point.data
        time = point.time
        base_path = config.base_path

        # GEOS
        GEOS_list = config.GEOS_list
        for j in range(len(GEOS_list)):
            value = GEOS_list[j]
            GEOS_path = base_path + os.path.sep + 'GEOS' + os.path.sep + date + os.path.sep + value + f'_{time}.tif'
            logger.info(f"Open {GEOS_path}")

            data_list = get_value_from_xy(GEOS_path, point)

            x = data_list[0]
            y = Gdaltiff(GEOS_path).getImg({'lat': point.lat, 'lon': point.lon})[1][1]
            # y = data.numpy()[j][1][1]

            if not (examin(x, y)):
                print(f'检验失败,第{index}行数据,字段{arr_list[j]}')


        # SILAM
        j = 6
        GEOS_path = base_path + os.path.sep + 'SILAM' + os.path.sep + date + os.path.sep + 'cnc_O3_gas_hybrid10' + f'_{time}.tif'
        logger.info(f"Open {GEOS_path}")

        data_list = get_value_from_xy(GEOS_path, point)

        x = data_list[0]
        y = Gdaltiff(GEOS_path).getImg({'lat': point.lat, 'lon': point.lon})[1][1]

        if not (examin(x, y)):
            print(f'检验失败,第{index}行数据,字段{arr_list[j]}')

        # TropOMI_O3_PR
        j = 7
        GEOS_path = base_path + os.path.sep + 'Tropomi' + os.path.sep + date + os.path.sep + 'TropOMI_O3_PR' + f'_.tif'
        logger.info(f"Open {GEOS_path}")

        data_list = get_value_from_xy(GEOS_path, point)

        x = data_list[0]
        y = Gdaltiff(GEOS_path).getImg({'lat': point.lat, 'lon': point.lon})[1][1]

        if not (examin(x, y)):
            print(f'检验失败,第{index}行数据,字段{arr_list[j]}')

        # LandCover
        LandCover = config.LandCover
        for k in range(len(LandCover)):
            value = LandCover[k]
            j = k + 8
            date1 = ''
            if int(date[-2:]) <= 17:

                date1 = '2022_05_09'
            else:
                date1 = '2022_05_25'

            GEOS_path = base_path + os.path.sep + 'LandCover' + os.path.sep + date1 + os.path.sep + value + f'.tif'
            logger.info(f"Open {GEOS_path}")

            data_list = get_value_from_xy(GEOS_path, point)

            x = data_list[0]
            y = Gdaltiff(GEOS_path).getImg({'lat': point.lat, 'lon': point.lon})[1][1]

            if not (examin(x, y)):
                print(f'检验失败,第{index}行数据,字段{arr_list[j]}')

    return


if __name__ == '__main__':
    examine_train()
