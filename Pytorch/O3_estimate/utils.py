import multiprocessing

import multitasking
import numpy as np
from osgeo import gdal
from Pytorch.O3_estimate.Resource import config

img_list = ['PS', 'T2M', 'TROPCOL_O3', 'U2M', 'V2M', 'ZPBL', 'SILAM', 'Tropomi', 'DEM', 'NDVI', 'POP', 'pri_sec']
path = r'Resource\math1.txt'


# 返回数据集中使用的mean,std
def get_math():
    mean_list = []
    std_list = []
    max_list = []
    min_list = []

    with open(path, 'r', encoding='utf-8') as f:
        imgs_info = f.readlines()
        imgs_info = list(map(lambda x: x.strip().split('\t'), imgs_info))

    txt = imgs_info

    for i in img_list:
        for j in txt:
            if (i in j[0]):
                # print(i,j[0])
                mean_list.append(j[3])
                std_list.append(j[4])
                max_list.append(j[1])
                min_list.append(j[2])

    # for i in range(12):
    #     print(img_list[i], mean_list[i], std_list[i])

    return mean_list, std_list, max_list, min_list


# 进行归一化
def normalization(data, max_data, min_data):
    min_data = float(min_data)
    _range = float(max_data) - min_data
    return (data - min_data) / _range


# 获取数组
def getImg(path, point):
    ratio = config.ratio
    x, y = config.img_size
    lat = float(point.lat)
    lon = float(point.lon)

    ds = gdal.Open(path)
    rows = ds.RasterYSize  # 行数
    cols = ds.RasterXSize  # 列数
    # bands = ds.RasterCount
    # Proj = ds.GetProjection()
    Transform = ds.GetGeoTransform()
    Bandarr = ds.GetRasterBand(1).ReadAsArray()
    # print(Bandarr.shape)
    del ds

    maxLatmain = Transform[3]
    # minLatmain = Transform[3] + rows * Transform[5]
    minLonmain = Transform[0]
    # maxLonmain = Transform[0] + cols * Transform[1]

    lat_value = int((maxLatmain - (lat)) / ratio)
    lon_value = int((lon - minLonmain) / ratio)

    # y_min = lat_value - int(y / 2)
    # y_max = y_min + y

    y_left = lat_value - int(y / 2)
    y_right = y_left + y

    x_left = lon_value - int(x / 2)
    x_right = x_left + x

    data = Bandarr[y_left:y_right, x_left:x_right]

    getdata = lambda x: Bandarr[lat_value - x: lat_value + x, lon_value - x:lon_value + x]
    # 如果数据在边缘位置 需要进行数组扩充
    if (x_left < 0):
        if (y_left < 0):
            value = lon_value if lon_value < lat_value else lat_value
        else:
            value = lon_value if lon_value < rows - 1 - lat_value else rows - 1 - lat_value
        data = getdata(value)
        return data

    if (y_left < 0):
        value = lat_value if lat_value < cols - 1 - lon_value else cols - 1 - lon_value
        data = getdata(value)
        return data

    if (y_right > rows - 1):
        if (x_right > cols - 1):
            value = rows - 1 - lat_value if rows - 1 - lat_value < cols - 1 - lon_value else cols - 1 - lon_value
        else:
            value = rows - 1 - lat_value if rows - 1 - lat_value < lon_value else lon_value
        data = getdata(value)
        return data

    if (x_right > cols - 1):
        value = cols - 1 - lon_value if cols - 1 - lon_value < lat_value else lat_value
        data = getdata(value)
        return data
    # data = Bandarr[0, :]

    return data


def padding_black(img):  # 如果尺寸太小可以扩充
    w, h = img.shape
    x, y = config.img_size

    data = img
    # data = img.reshape((1, w * h))[0, :]
    # print(data.shape)

    count = x * y
    time = int(x / w) if int(x / w) < int(y / h) else int(y / h)

    data = np.repeat(data, time, axis=1)
    data = np.repeat(data, time, axis=0)
    # print(data.shape)

    x1 = x - data.shape[0]
    y1 = y - data.shape[1]
    list = []
    for i in data:
        j = i.tolist()
        temp = j + [i[-1] for k in range(y1)]
        list.append(temp)

    for i in range(x1):
        list.append(list[-1])

    img = np.array(list)
    # temp = [data[-1] for j in range(count - (w * h * time))]
    # list += temp
    #
    # img = np.array(list).reshape(x,y)
    return img


def data_examine(img):  # 如果尺寸太小可以扩充
    w, h = img.shape
    x, y = config.img_size
    data = img

    if (data[1, 0] < -10000):
        data = np.delete(data, 0, axis=1)
    else:
        data = np.delete(data, -1, axis=1)
    if (data[0, 1] < -10000):
        data = np.delete(data, 0, axis=0)
    else:
        data = np.delete(data, -1, axis=0)

    if (data.min() < -1000000):
        print('数据错误，最小值小于-100000')
        # sys.exit()
    return data



def addList( item, i,return_dict):
    path = item.img_path[i]
    img = getImg(path, item)
    img = data_examine(img)
    img = padding_black(img)

    return_dict[i] = img

def getImgMul(item):

    manager = multiprocessing.Manager()
    # 构造返回值存储结构，本质是共享内存方式
    return_dict = manager.dict()
    jobs = []
    for i in range(12):
        # 将构造的返回值存储结构传递给多线程执行函数，并标识各个线程id
        p = multiprocessing.Process(target=addList, args=(item,i, return_dict))
        jobs.append(p)
        p.start()

    for proc in jobs:
        proc.join()

    # 所有线程处理完毕后，遍历结果输出
    list = []
    value = return_dict.items()
    for i in range(12):

        for id, arr in value:
            if( i == int(id)):
                list.append(arr)


    return list


if __name__ == '__main__':
    get_math()
