# Athor xyz


from urllib import request

import ssl
from contextlib import closing
import requests, os
import time
# 引用本地文件
from utilS import check_file
import time,sys
sys.path.insert(0,os.path.dirname(os.getcwd()))

log1 =check_file.log



# 配置下载设置

ssl._create_default_https_context = ssl._create_unverified_context  # 取消全局验证
requests.packages.urllib3.disable_warnings()
# 跳过代理
proxies = {
    "http": None,
    "https": None,
}


'''
下载器
'''

# 下载
def download_file(download_url, download_path):
    video_name = os.path.basename(download_path)

    startime = time.time()
    content_size1 = 0
    try:
        with request.urlopen(download_url) as file:
            pass
    except Exception as reason:
        print(repr(reason))
        print('------------------------------该url不存在-----------------------------')
        return

    try:
        with closing(requests.get(download_url, timeout=10, verify=False, stream=True, proxies=proxies)) as response:
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
        log1.info(f'下载{os.path.basename(download_path)}耗时:{endtime - startime}秒')

    except Exception as reason:
        print(f"{video_name}   下载失败！！！")
        print(reason)

    finally:
        # 验证文件完整性
        check_file.down_check(download_path, content_size1)
