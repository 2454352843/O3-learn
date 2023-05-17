# Athor xyz
# 根据连接下载文件
# 使用请告知
import datetime
from datetime import date, timedelta
import logging
import ssl
from contextlib import closing
import requests, os
import time
# 导入用于多线程操作的库
# 这样子仅需要在自定义的函数前面使用装饰器即可将函数开启新的线程
import multitasking
import signal

# 按快捷键 ctrl + c 终止已开启的全部线程
from urllib import request

from dataset.GEOS.CF.utils.check_file import down_check

signal.signal(signal.SIGINT, multitasking.killall)
multitasking.set_max_threads(4)  # 最大线程数为4
ssl._create_default_https_context = ssl._create_unverified_context#取消全局验证

basepath = r'H:\work\python\data\GEOS_CF\\'
basepath_ZPBL = r'H:\data\5. GEOS-CF\weather' + os.path.sep
bathurl = 'https://portal.nccs.nasa.gov/datashare/gmao/geos-cf/v1/forecast/'
o3path = 'down_cf_o3.txt'
weatherpath = 'down_cf_weather.txt'

# 跳过代理
proxies = {
  "http": None,
  "https": None,
}


# wget 下载
@multitasking.task
def wget_down(url, path):
    wget.download(url, path)


# IDM下载
# @multitasking.task
def IDMdownload(DownUrl, DownPath, FileName):
    IDMPath = r"C:\myDepot\soft\work\IDM\Internet Download Manager\\"
    os.chdir(IDMPath)
    IDM = "IDMan.exe"
    command = ' '.join([IDM, '/d', DownUrl, '/p', DownPath, '/f', FileName, '/q'])
    print(command)
    os.system(command)


# 下载
# @multitasking.task
def download_video(download_url, download_path):
    video_name = os.path.basename(download_path)
    if (os.path.exists(download_path)):
        # print(f"{video_name} exist".format(video_name))
        return
    startime = time.time()
    # print(f"star down {video_name}".format(video_name))
    content_size1 = 0
    try:
        with request.urlopen( download_url) as file:
            pass
    except Exception as reason:
        print(repr(reason))
        print('------------------------------该url不存在-----------------------------')
        print('------------------------------该url不存在-----------------------------')
        print('------------------------------该url不存在-----------------------------')
        return

    try:
        with closing(requests.get(download_url, timeout=10, verify=False, stream=True,proxies=proxies)) as response:
            chunk_size = 1024  # 单次请求最大值
            content_size = int(response.headers['content-length'])  # 文件总大小
            content_size1 = content_size
            data_count = 0  # 当前已传输的大小
            with open(download_path, "wb") as file:
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)
                    done_block = int((data_count / content_size) * 50)  # 已经下载的文件大小
                    data_count = data_count + len(data)  # 实时进度条进度
                    now_jd = (data_count / content_size) * 100  # %% 表示%
                    print("\r %s [%s%s] %d%% " % (
                        video_name + "---->", done_block * '█', ' ' * (50 - 1 - done_block), now_jd), end=" ")

        endtime = time.time()
        print('耗时:', endtime - startime, '秒')

    except Exception as reason:
        print(f"{video_name}   下载失败！！！")

        print(reason)

    finally:
        #验证文件完整性
        down_check(download_path , content_size1)


def write_txt_O3(line):
    file = open(o3path, 'a')

    file.write(line)
    file.write('\n')

def write_txt_weather(line):
    file = open(weatherpath, 'a')

    file.write(line)
    file.write('\n')


# 臭氧数据下载
def GEOS_CF_scrip(date):

    month = date[:2]
    day = date[2:]

    for i in range(6):
        stardate = date_count(i, day, month)

        for j in range(24):
            if (i == 0):
                j = j + 12

            starhour = j
            if (starhour < 10):
                starhour = '0' + str(starhour)
            filename = 'M{month}/D{day}/H12/GEOS-CF.v01.fcst.aqc_tavg_1hr_g1440x721_v1.2022{date}_12z+2022{stardate}_{starhour}30z.nc4'.format(
                date=date, month=month, day=day, stardate=stardate, starhour=starhour)
            url = bathurl + filename

            path = basepath + filename

            ### 下载数据




            print(f'开始下载 {url}'.format(url=url))
            print(path)
            if (os.path.exists(path)):
                # print(f"{path} exist".format(path))
                continue
            # download_video(url, path)
            print("调用下载结束 休眠10S")
            time.sleep(10)


            # 导出连接到文件中
            # write_txt_O3(url)
            if (i == 5):
                if (j == 11):
                    break
            if (j >= 23):
                break


        multitasking.wait_for_tasks()

# ZPBL数据下载
#根据日期下载数据
def GEOS_CF_ZPBL_scrip(year,date):

    month = date[:2]
    day = date[2:]

    for i in range(6):
        stardate = date_count(i, day, month,year)

        for j in range(24):
            if (i == 0):
                j = j + 12
                if(j >= 24):
                    continue
            if(i == 5 and j >= 12):
                continue
            starhour = j
            if (starhour < 10):
                starhour = '0' + str(starhour)
            # https://portal.nccs.nasa.gov/datashare/gmao/geos-cf/v1/forecast/Y2023/M02/D09/H12/GEOS-CF.v01.fcst.met_tavg_1hr_g1440x721_x1.20230209_12z+20230209_1230z.nc4
            # https://portal.nccs.nasa.gov/datashare/gmao/geos-cf/v1/forecast/Y2023/M01/D09/H12/GEOS-CF.v01.fcst.met_tavg_1hr_g1440x721_x1.20230109_12z+20230109_1230z.nc4
            filename = 'Y{year}/M{month}/D{day}/H12/GEOS-CF.v01.fcst.met_tavg_1hr_g1440x721_x1.{year}{date}_12z+{stardate}_{starhour}30z.nc4'.format(
                year = year,date=date, month=month, day=day, stardate=stardate, starhour=starhour)
            url = bathurl + filename

            path = basepath_ZPBL + filename.split('/')[-1]



            ### 下载数据

            # 导出连接到文件中
            # write_txt_weather(url)

            # 1.判断是否存在
            if (os.path.exists(path)):
                # print(f"{path} exist".format(path))
                continue

            print(f'开始下载 {url}'.format(url=url))

            download_video(url, path)
            print("调用下载结束 休眠10S")
            time.sleep(10)

            if (i == 5):
                if (j == 11):
                    break
            if (j >= 23):
                break


    multitasking.wait_for_tasks()

    ##  检验
    print("开始检验")
    k = jianyan_ZPBL(date)

    if (k < 0):
        print('sleep 10S')
        time.sleep(10)
        GEOS_CF_ZPBL_scrip(year,date)


# 检验代码 检查当日数据格式和数据大小，判断当前数据是否够16个
def jianyan_ZPBL(date):
    mark = 0
    list_silam = os.listdir(basepath_ZPBL)
    count = 0
    for i in list_silam:

        if not (date in i[-27:-23]):
            continue

        path = basepath_ZPBL + i

        if not ("nc" in path):
            os.remove(path)
            continue

        count += 1
        size = os.stat(path).st_size

       #28672000
        if (size < 28672000):
            try:
                os.remove(path)
            except Exception:
                print(Exception)
            finally:
                mark = -1

    print(f'{date}有{count}个数据,还差 {120 - count}个')
    if (count< 120):

        mark = -1
    if (mark < 0):
        return -1
    return  1


def date_count(i, day, mouth,year):
    # starday  没有计算闰年
    markDay = int(i)
    stardate = datetime.date(int(year),int(mouth),int(day)) + datetime.timedelta(days=markDay)



    # starday = int(day) + markDay
    # markstarmonth = 0
    # if (starday > 28):
    #     if (int(mouth) == 2):
    #         starday = starday - 28
    #         markstarmonth = 1
    #
    #     elif (starday > 30):
    #         if (int(mouth) in [4, 6, 9, 11]):
    #             starday = starday - 30
    #             markstarmonth = 1
    #         else:
    #             if (starday > 31):
    #                 starday = starday - 31
    #                 markstarmonth = 1
    #
    # # starmonth
    # starmonth = int(mouth) + markstarmonth
    # if (starmonth > 12):
    #     starmonth = starmonth - 12
    # if (starmonth < 10):
    #     starmonth = '0' + str(starmonth)
    # if (starday < 10):
    #     starday = '0' + str(starday)
    return stardate.strftime("%Y%m%d")






#下载臭氧数据
def main_O3():
    # GEOS_CF_scrip('1001')
    given_date = date.today().replace(day=1)
    i = 1
    while (i < 23):
        date1 =  (given_date + timedelta(days=i)).strftime("%m%d")
        print(date1)
        GEOS_CF_scrip(date1)
        i = i + 1


#下载环境数据
def main_ZPBL():
    # GEOS_CF_scrip('1001')、

    for i  in range(16):
        value = i-16
        down_date = (date.today() + timedelta(days=value)).strftime("%m%d")
        year = (date.today() + timedelta(days=value)).strftime("%Y")

        print("开始下载{n}号数据".format(n = down_date))
        # if('18' in down_date):
        #     continue
        GEOS_CF_ZPBL_scrip(year,down_date)
        # jianyan_ZPBL(down_date)



# 每日自动调用mian
#十三点进行下载
def automatic_ZPBL():
    main_ZPBL()
    i = 1
    day = 24
    while (True):
        hour =    time.strftime('%H', time.localtime(time.time()))
        print('当前时间为 {n} hour'.format(n = hour))

        time.sleep(600)
        if (str(hour) == '13'):

            main_ZPBL()
            time.sleep(3600)




if __name__ == '__main__':
    automatic_ZPBL()
    # write_txt()


