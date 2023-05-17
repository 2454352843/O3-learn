# Athor xyz
# 根据连接下载文件
# 使用请告知
import datetime
from datetime import date, timedelta
import logging
# import wget
from contextlib import closing
import requests, os
import time
# 导入用于多线程操作的库
# 这样子仅需要在自定义的函数前面使用装饰器即可将函数开启新的线程
import multitasking
import signal
from subprocess import call

# 按快捷键 ctrl + c 终止已开启的全部线程
signal.signal(signal.SIGINT, multitasking.killall)
multitasking.set_max_threads(4)  # 最大线程数为cpu核数*2

import urllib3

urllib3.disable_warnings()
basepath = r'H:\data\3. SILAM\silam_china_v5_5_1'
bathurl = 'https://silam.fmi.fi/thredds/ncss/silam_china_v5_5_1/files'

# 跳过代理
proxies = {
    "http": None,
    "https": None,
}


# wget 下载
@multitasking.task
def wget_down(url, path):
    wget.download(url, path)


# 下载
@multitasking.task
def download_video1(download_url, download_path):
    video_name = os.path.basename(download_path)
    if (os.path.exists(download_path)):
        print(f"{video_name} exist".format(video_name))
        return
    startime = time.time()
    print(f"{download_url}".format(download_url))
    content_size1 = 0
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

        # 验证文件完整性
        down_check(download_path, content_size1)

    except Exception as reason:
        print(f"{video_name}   下载失败！！！")

        print(reason)


# 检验下载文件是否完成
# download_path 本地文件  tontent_size  请求文件大小
def down_check(download_path, content_size):
    if not (os.path.exists(download_path)):
        print(f"{download_path} not exist".format(download_path))
        return

    print('开始校验文件完整性')
    file_count = os.stat(download_path).st_size
    time.sleep(3)
    if (file_count < content_size - 1024):
        os.remove(download_path)
        print("检验失败")

    else:
        print("检验结束")


# 下载
@multitasking.task
def download_video(download_url, download_path):
    video_name = os.path.basename(download_path)
    if (os.path.exists(download_path)):
        print(f"{video_name} exist".format(video_name))
        return
    startime = time.time()
    print(f"star down {video_name}".format(video_name))
    print('下载连接: {http}'.format(http=download_url))

    with closing(requests.get(download_url, timeout=10, verify=False, stream=True, proxies=proxies)) as response:
        chunk_size = 1024  # 单次请求最大值
        content_size = int(response.headers['content-length'])  # 文件总大小
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


# 化学模式数据silam_scrip下载
def silam_scrip(date):
    str_data = str(date)
    year = str_data.split('-')[0]
    mouth = str_data.split('-')[1]
    day = str_data.split('-')[2]

    hour = 1
    # 遍历下载每天的数据
    for i in range(16):  # 1-16

        # 小时计算

        # hour
        hour = 1 + (i) * 6
        if len(str(hour)) == 1:
            hour = '0' + str(hour)

        # endhour
        enddaymark = 0
        mark = i % 4
        endhour = 6 + mark * 6
        if (endhour == 24):
            endhour = 0
            enddaymark = 1
        if len(str(endhour)) == 1:
            endhour = '0' + str(endhour)

        # starhour
        starhour = 1 + mark * 6
        if len(str(starhour)) == 1:
            starhour = '0' + str(starhour)

        # 日期计算

        starmonth, starday, staryear = date_count1(i, day, mouth , year)


        enddate = datetime.date(int(staryear), int(starmonth), int(starday)) + datetime.timedelta(enddaymark)
        endday = str(enddate).split('-')[2]
        endmouth = str(enddate).split('-')[1]
        endyear = str(enddate).split('-')[0]
        # markendmonth = 0
        # if (endday > 28):
        #     if (int(starmonth) == 2):
        #         endday = endday - 28
        #         markendmonth = 1
        #
        #     elif (endday > 30):
        #         if (int(starmonth) in [4, 6, 9, 11]):
        #             endday = endday - 30
        #             markendmonth = 1
        #         else:
        #             if (endday > 31):
        #                 endday = endday - 31
        #                 markendmonth = 1
        #
        # if (starday < 10):
        #     starday = '0' + str(starday)
        # if (endday < 10):
        #     endday = '0' + str(endday)
        #
        # endmonth = int(starmonth) + markendmonth

        # 路径拼接
        # https://silam.fmi.fi/thredds/ncss/silam_china_v5_5_1/files/SILAM-AQ-china_v5_5_1_2022110100_085.nc4?var=BLH&var=NO2_tropcol&var=O3_tropcol&var=SO2_tropcol&var=dd_CO_gas&var=dd_EC_m_50&var=ocd_EC_m_50_w380&var=ocd_EC_m_50_w550&var=wd_CO_gas&var=cnc_CO_gas&var=cnc_EC_m_50&var=cnc_O3_gas&disableLLSubset=on&disableProjSubset=on&horizStride=1&time_start=2022-11-04T13%3A00%3A00Z&time_end=2022-11-04T18%3A00%3A00Z&timeStride=1&vertCoord=&accept=netcdf
        # https://silam.fmi.fi/thredds/ncss/silam_china_v5_5_1/files/SILAM-AQ-china_v5_5_1_2022110200_001.nc4?&disableLLSubset=on&disableProjSubset=on&horizStride=1&time_start=2022-11-02T01%3A00%3A00Z&time_end=2022-11-02T06%3A00%3A00Z&timeStride=1&vertCoord=&accept=netcdf
        # https://silam.fmi.fi/thredds/ncss/silam_china_v5_5_1/files/SILAM-AQ-china_v5_5_1_2022110600_001.nc4?&disableLLSubset=on&disableProjSubset=on&horizStride=1&time_start=2022-11-06T01%3A00%3A00Z&time_end=2022-11-06T06%3A00%3A00Z&timeStride=1&vertCoord=&accept=netcdf
        #           SILAM-AQ-china_v5_5_1_2022122800_001.nc4?var=O3_tropcol&disableLLSubset=on&disableProjSubset=on&horizStride=1&time_start=2022-12-28T01%3A00%3A00Z&time_end=2022-12-28T06%3A00%3A00Z&timeStride=1&vertCoord=&accept=netcdf
        #           SILAM-AQ-china_v5_5_1_20222022-12-2800_007.nc4?var=BLH&var=NO2_tropcol&var=O3_tropcol&var=SO2_tropcol&var=dd_CO_gas&var=dd_EC_m_50&var=ocd_EC_m_50_w380&var=ocd_EC_m_50_w550&var=wd_CO_gas&var=cnc_CO_gas&var=cnc_EC_m_50&var=cnc_O3_gas&disableLLSubset=on&disableProjSubset=on&horizStride=1&time_start=2022-12-28T07%3A00%3A00Z&time_end=2022-12-28T12%3A00%3A00Z&timeStride=1&vertCoord=&accept=netcdf
        filename = 'SILAM-AQ-china_v5_5_1_{year}{date}00_0{hour}.nc4?var=BLH&var=NO2_tropcol&var=O3_tropcol&var=SO2_tropcol&var=dd_CO_gas&var=dd_EC_m_50&var=ocd_EC_m_50_w380&var=ocd_EC_m_50_w550&var=wd_CO_gas&var=cnc_CO_gas&var=cnc_EC_m_50&var=cnc_O3_gas&disableLLSubset=on&disableProjSubset=on&horizStride=1&time_start={staryear}-{starmonth}-{starday}T{starhour}%3A00%3A00Z&time_end={endyear}-{endmonth}-{endday}T{endhour}%3A00%3A00Z&timeStride=1&vertCoord=&accept=netcdf' \
            .format(year=year, date=mouth+day, hour=hour,
                    staryear=staryear, starmonth=starmonth, starday=starday, starhour=starhour,
                    endyear = endyear,endmonth=endmouth, endday=endday, endhour=endhour)
        url = bathurl + '/' + filename

        basename = filename.split('?')[0]
        path = basepath + os.path.sep + basename

        if (os.path.exists(path)):
            print(f"{path} exist".format(path))
            continue
        download_video1(url, path)
        print("调用下载结束 休眠30S")
        time.sleep(30)

        # IDMdownload(url,path,basename)
    multitasking.wait_for_tasks()
    print("{date} 下载结束".format(date=date))
    print("开始检验...")
    k = jianyan(date)
    print("检验结束")
    if (k < 0):
        print('sleep 60S')
        time.sleep(60)
        silam_scrip(date)


def date_count1(i, day, mouth, year):
    markDay = int(i / 4)
    data = datetime.date(int(year), int(mouth), int(day)) + datetime.timedelta(days=markDay)
    starmonth = str(data).split('-')[1]
    starday = str(data).split('-')[2]
    staryear = str(data).split('-')[0]
    return starmonth, starday, staryear


def date_count(i, day, mouth):
    # starday  没有计算闰年
    markDay = int(i / 4)
    starday = int(day) + markDay
    markstarmonth = 0
    if (starday > 28):
        if (int(mouth) == 2):
            starday = starday - 28
            markstarmonth = 1

        elif (starday > 30):
            if (int(mouth) in [4, 6, 9, 11]):
                starday = starday - 30
                markstarmonth = 1
            else:
                if (starday > 31):
                    starday = starday - 31
                    markstarmonth = 1

    # starmonth
    starmonth = int(mouth) + markstarmonth
    if (starmonth > 12):
        starmonth = starmonth - 12

    return starmonth, starday


@multitasking.task
def IDMdownload(DownUrl, DownPath, FileName):
    IDMPath = r"C:\myDepot\soft\work\IDM\Internet Download Manager\\"
    os.chdir(IDMPath)
    IDM = "IDMan.exe"

    call([IDM, '/d', DownUrl, '/p', DownPath, '/f', FileName, '/q'])
    call([IDM, '/s'])


# 检验代码 检查当日数据格式和数据大小，判断当前数据是否够16个
def jianyan(date1):
    date1 = str(date1)
    data = ''
    for i in date1.split('-'):
        data = data + i
    mark = 0
    list_silam = os.listdir(basepath)
    count = 0

    for i in list_silam:
        if not (str(data) in i):
            continue
        count += 1
        path = basepath + os.path.sep + i
        if not ("nc" in path):
            os.remove(path)
            continue
        size = os.stat(path).st_size
        # 103284736
        # 103559260
        # 293346180
        # 293309621
        if (size < 293309621):
            try:
                os.remove(path)
            except Exception:
                print(Exception)
            finally:
                mark = -1

    if (mark < 0):
        return -1
    list_new = os.listdir(basepath)
    if (len(list_new) != len(list_silam)):
        list1 = set(list_silam).difference((set(list_new)))
        list1 = list(list1)
        print("检查后删除的不符合数据共{n}个".format(n=len(list1)))
        count = 1
        for i in list1:
            print("第{i}个为:{k}".format(i=count, k=i))
            count += 1

        return -1
    elif (count < 16):
        print("当日数据下载{n}个,还缺少数据".format(n=count))
        return -1
    else:
        return 1


def main():
    silam_scrip((date.today() + timedelta(days=-3)))
    silam_scrip((date.today() + timedelta(days=-2)))
    silam_scrip((date.today() + timedelta(days=-1)))
    silam_scrip((date.today()))


# 每日自动调用mian
def automatic():
    main()
    i = 1
    day = 24
    while (True):
        hour = time.strftime('%H', time.localtime(time.time()))
        print('当前时间为 {n} hour'.format(n=hour))

        time.sleep(600)
        if (str(hour) == '13'):
            main()
            time.sleep(3600)


if __name__ == '__main__':
    automatic()
