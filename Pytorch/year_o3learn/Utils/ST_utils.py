import random
from Pytorch.year_o3learn.Resource import config
import calendar

'''
转换函数
'''


def get_x1(x, x_bar):
    if (x < 2 * x_bar and x >= 0):
        x1 = (2 * x_bar - x) / (2 * x_bar)
    else:
        x1 = 0
    return x1


def get_xn(n, x, x_bar):
    xn_bar = (n - 0.5) * x_bar

    if (x >= (n - 1) * x_bar and x < n * x_bar):
        xn = (x_bar - abs(xn_bar - x)) / x_bar
    elif (x > (n - 1.5) * x_bar and x < (n - 1) * x_bar):
        xn = (x - (n - 1.5) * x_bar) / x_bar
    elif (x >= n * x_bar and x < (n + 0.5) * x_bar):
        xn = ((n + 0.5) * x_bar - x) / x_bar
    else:
        xn = 0

    return xn


def get_xm(m, x, x_bar):
    if (x < m * x_bar and x >= (m - 2) * x_bar):
        xm = (x - (m - 2) * x_bar) / (2 * x_bar)
    else:
        xm = 0

    return xm


'''
时空数据转换，输入行列数，输出m*m矩阵
'''


# 空间镶嵌
def spatial_embedding(lat, lon):
    m = config.img_size[0]
    lat_value = config.lat_HB
    lon_value = config.lon_HB

    # 纬度lat计算
    lat_list = []
    lat_bar = int(lat_value / m)
    lat_list.append(get_x1(lat, lat_bar))

    for i in range((m - 2)):
        n = i + 2
        lat_list.append(get_xn(n, lat, lat_bar))

    lat_list.append(get_xm(m, lat, lat_bar + lat_value % m))

    # 经度lon计算
    lon_list = []
    lon_bar = int(lon_value / m)
    lon_list.append(get_x1(lon, lon_bar))

    for i in range((m - 2)):
        n = i + 2
        lon_list.append(get_xn(n, lon, lon_bar))

    lon_list.append(get_xm(m, lon, lon_bar + lon_value % m))

    # 经纬度向量计算
    data = []
    for i in range(m):
        row = []
        for j in range(m):
            row.append(lon_list[j] * lat_list[i])
        data.append(row)

    # 打印
    # print(f'lon_list:{lon_list}')
    # print(f'lat_list:{lat_list}')
    return data


# 日期镶嵌
def date_embedding(date):
    # 2022_05_23

    # 参数读取
    m = config.img_size[0]
    month = int(date.split('_')[1])
    day = int(date.split('_')[2])

    # 1 日期转换 月，日-> （0，365）
    date_value = 0
    for i in range(month - 1):
        date_value += int(calendar.monthrange(2022, i + 1)[1])
    date_value += day

    # 2 向量转换
    date_list = []
    date_bar = int(365 / m)
    date_list.append(get_x1(date_value, date_bar))

    for i in range(m - 2):
        n = i + 2
        date_list.append(get_xn(n, date_value, date_bar))

    date_list.append(get_xm(m, date_value, date_bar + 365 % m))

    # 3 生成矩阵
    data = []
    for i in range(m):
        row = []
        for j in range(m):
            if (i == j):
                row.append(date_list[i])
            else:
                row.append(0)
        data.append(row)

    # 输出打印
    # print(f'date_value:{date_value}')
    # print(f'date_bar: {date_bar}')
    # print(f'date_list:{date_list}')
    return data


# 时间镶嵌
def time_embedding(time):
    # 8-20 一共13个小时
    time = int(time)
    m = config.img_size[0]
    time_bar = int(24 / m)

    time_list = []
    time_list.append(get_x1(time, time_bar))
    for i in range(m - 2):
        n = i + 2
        time_list.append(get_xn(n, time, time_bar))

    time_list.append(get_xm(m, time, time_bar + 24 % m))

    # 3 生成矩阵
    data = []
    for i in range(m):
        row = []
        for j in range(m):
            if (i == j):
                row.append(time_list[i])
            else:
                row.append(0)
        data.append(row)

    # 输出打印
    # print(f'date_value:{time}')
    # print(f'date_bar: {time_bar}')
    # print(f'date_list:{time_list}')
    return data


def test_spatial():
    lat_value = config.lat_value
    lon_value = config.lon_value
    m = config.img_size[0]

    lat = random.randint(0, lat_value)
    lon = random.randint(0, lon_value)

    print()
    print(f'lon_value:{lon_value} , lat_value:{lat_value}')
    print(f'lon_bar:{int(lon_value / m)} , lat_bar:{int(lat_value / m)}')
    print(f'lon:{lon} , lat:{lat}')

    data = spatial_embedding(lat, lon)

    # 打印
    for i in data:
        print(i)


def test_data():
    m = config.img_size[0]

    date = '2022_' + str(random.randint(1, 12)) + f'_{str(random.randint(1, 30))}'
    # date='2022_6_28'
    print()
    print(f'date:{date} ')
    data = date_embedding(date)

    # 打印
    for i in data:
        print(i)


def test_time():
    m = config.img_size[0]

    time = random.randint(0, 23)
    time = 16
    # date='2022_6_28'
    print()
    print(f'time:{time} ')
    data = time_embedding(time)

    # 打印
    for i in data:
        print(i)


if __name__ == '__main__':
    test_time()
