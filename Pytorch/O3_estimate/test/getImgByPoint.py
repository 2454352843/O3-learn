import numpy as np
from osgeo import gdal
from PIL import Image

path = r'D:\work\python\data\TROPCOL_O3\2021_12_01\00\TROPCOL_O3.tif'
ratio = 0.25


class Point(object):
    def __init__(self, value):
        self.value = value

        self.lat = value[0]
        self.lon = value[1]
        self.data = value[2]
        self.time = value[3]
        self.key = value[4]

        self.img_path = value[5:-1]

        self.PS_path = value[5]
        self.T2M_path = value[6]
        self.GEOS_Oznone_path = value[7]
        self.U2M_path = value[8]
        self.V2M_path = value[9]
        self.ZPBL_path = value[10]
        self.SILAM_path = value[11]
        self.Tropomi_path = value[12]
        self.DEM_path = value[13]
        self.NDVI_path = value[14]
        # self.NDVI_resample_path = value[15]
        self.POP_path = value[15]
        self.pri_sec_path = value[16]
        self.tertiary_path = value[17]

    def __str__(self):
        return str(self.value)


def getImgBysize(path, point):
    x, y = (50, 50)
    lat = point.lat
    lon = point.lon

    ds = gdal.Open(path)
    rows = ds.RasterYSize  # 行数
    cols = ds.RasterXSize  # 列数
    # bands = ds.RasterCount
    # Proj = ds.GetProjection()
    Transform = ds.GetGeoTransform()
    Bandarr = ds.GetRasterBand(1).ReadAsArray()
    # print(Bandarr.shape)
    del ds

    maxLatmain = Transform[3]  # 60.0
    minLatmain = Transform[3] + rows * Transform[5]  # 17.0
    minLonmain = Transform[0]  # 70.0
    maxLonmain = Transform[0] + cols * Transform[1]  # 137.0

    lat_value = int((maxLatmain - lat) / ratio)
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
    x, y = (50, 50)

    data = img
    # data = img.reshape((1, w * h))[0, :]
    print(data.shape)

    count = x * y
    time = int(x / w) if int(x / w) < int(y / h) else int(y / h)


    data = np.repeat(data, time, axis=1)
    data = np.repeat(data, time, axis=0)
    print(data.shape)


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


if __name__ == '__main__':
    value = [19, 71, "", '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']
    point = Point(value)
    # getImgB(path, (50, 50), point)

    data = getImgBysize(path, point)
    print(data.shape)

    img = padding_black(data)
