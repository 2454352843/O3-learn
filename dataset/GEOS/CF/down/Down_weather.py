# Athor xyz
# 根据连接下载文件
# 使用请告知

# 导入用于多线程操作的库
# 这样子仅需要在自定义的函数前面使用装饰器即可将函数开启新的线程
import multitasking
import signal
# 按快捷键 ctrl + c 终止已开启的全部线程
from urllib import request
import datetime
from datetime import date, timedelta
import ssl
from contextlib import closing
import requests, os
import time
# 引用本地文件
from utilS import check_file
from utilS.down_drive import download_file
import Config

log1 = check_file.log

# 配置下载设置
signal.signal(signal.SIGINT, multitasking.killall)
multitasking.set_max_threads(4)  # 最大线程数为4
ssl._create_default_https_context = ssl._create_unverified_context  # 取消全局验证
requests.packages.urllib3.disable_warnings()
# 跳过代理
proxies = {
    "http": None,
    "https": None,
}

'''

'''

basepath_weather = Config.basepath_weather
baseurl = Config.baseurl


# wget 下载
@multitasking.task
def wget_down(url, path):
    wget.download(url, path)


# IDM下载
def IDMdownload(DownUrl, DownPath, FileName):
    IDMPath = r"C:\myDepot\soft\work\IDM\Internet Download Manager\\"
    os.chdir(IDMPath)
    IDM = "IDMan.exe"
    command = ' '.join([IDM, '/d', DownUrl, '/p', DownPath, '/f', FileName, '/q'])
    print(command)
    os.system(command)





# ZPBL数据下载
# 根据日期下载数据
def GEOS_CF_weather_scrip(year, date):
    month = date[:2]
    day = date[2:]

    # 下载后续48小时数据
    for i in range(48):
        # 1.生成日期
        stardate, starhour = date_count(i, day, month, year)
        # 2. 生成下载连接
        filename = 'Y{year}/M{month}/D{day}/H12/GEOS-CF.v01.fcst.met_tavg_1hr_g1440x721_x1.{year}{date}_12z+{stardate}_{starhour}30z.nc4'.format(
            year=year, date=date, month=month, day=day, stardate=stardate, starhour=starhour)
        url = baseurl + filename

        folder = basepath_weather + f'{year}_{month}_{day}'
        path = folder + os.path.sep + filename.split('/')[-1]

        # 3.下载数据

        # 3.1判断是否存在
        if not os.path.exists(folder):
            os.makedirs(folder)
        if (os.path.exists(path)):
            continue

        # 3.2调用下载
        log1.info(f'开始调用下载 {url}')
        download_file(url, path)
        print("\r调用下载结束 休眠10S", end='')
        time.sleep(10)
        print('\r', end='\n')

    multitasking.wait_for_tasks()

    ##  检验
    print("开始检验")
    k = examine_weather(date,folder)

    if (k < 0):

        time.sleep(10)
        GEOS_CF_weather_scrip(year, date)


# 检验代码 检查当日数据格式和数据大小，判断当前数据是否够16个
def examine_weather(date,folder):
    mark = 0
    list_silam = os.listdir(folder)
    count = 0
    for i in list_silam:

        if not (date in i[-27:-23]):
            continue

        path = folder +os.path.sep+ i

        if not ("nc" in path):
            os.remove(path)
            continue

        count += 1
        size = os.stat(path).st_size

        # 28672000
        if (size < 28672000):
            try:
                os.remove(path)
            except Exception:
                print(Exception)
            finally:
                mark = -1

    log1.info(f'{date}有{count}个数据,还差 {48 - count}个')
    if (count < 48):
        mark = -1
    if (mark < 0):
        return -1
    return 1


def date_count(i, day, mouth, year):
    mark = int(i)
    stardate = datetime.datetime(int(year), int(mouth), int(day), 12) + datetime.timedelta(hours=mark)
    return stardate.strftime("%Y%m%d"), stardate.strftime("%H")


# 下载环境数据
def main_weather():
    # GEOS_CF_scrip('1001')、

    # 下载过去16天的数据
    for i in range(16):
        value = i - 16
        down_date = (date.today() + timedelta(days=value)).strftime("%m%d")
        year = (date.today() + timedelta(days=value)).strftime("%Y")

        log1.info(f"开始下载{down_date[:2]}_{down_date[2:]}号weather数据")
        GEOS_CF_weather_scrip(year, down_date)


def automatic_weather():
    main_weather()
    while (True):
        hour = time.strftime('%H:%m:%S', time.localtime(time.time()))
        print('\r 当前时间为 {n},程序开始休眠'.format(n=hour),end='')
        time.sleep(1)
        print('\r', end='')

        if (str(hour) == '13'):
            main_weather()
            time.sleep(3600)


if __name__ == '__main__':
    automatic_weather()
