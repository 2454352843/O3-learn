# coding: utf-8
# @Author: Ruan
# coding:utf-8

### 对于开发后的程序为了防止被人篡改
### 可以使用b模式将文件读取后
### 对文件进行hash处理
### 仅需要对照结果与我们开发时计算的结果是否相同即可
### 并且结果仅需要一串md5值即可


### 小型文件校验
### 创建两个文本文件,其中第二个文件多了一个字符串8
import hashlib
import os.path
import time


def check_small_file(file_path, enc_type=hashlib.md5()):
    """
        该方法会通过for循环以字节流读取文件
        并且通过updata方法添加到md5对象中进行校验
        如果用于大文件,则会校验很慢
         :param file_path 文件路径
         :param enc_type 加密方式,传入hashlib方法
    """
    enc_obj = enc_type
    with open(file_path, 'rb') as f:
        for line in f:
            enc_obj.update(line)
    return enc_obj.hexdigest()


def check_big_file(file_path: str, check_frequency: int = 10, check_once_bytes=100, enc_type=hashlib.md5()):
    """
         该方法用于大文件校验
         通过seek方法移动文件指针
         保证对文件每10%的地方进行一次读取,并校验其完整性！
         :param file_path 文件路径
         :param check_frequency 校验次数默认10,填写几次则会分个区间去读取并校验
         :param enc_type 加密方式,传入hashlib方法
         :tips 如果文件过小,可能会出现校验出错的文件,所以该方法一般用于大型文件校验
    """
    # 获取文件的字节数(方法1)
    file_bytes = os.path.getsize(file_path)
    enc_obj = enc_type
    with open(file_path, 'rb') as f:
        # 获取文件的字节数(方法2)
        f.seek(0, 2)  # 将文件指针移动到末尾
        file_bytes = f.tell()  # 获取末尾的指针值 -> 字节总数
        check_bytes = file_bytes // check_frequency  # 每次移动的文件字节数
        for i in range(check_frequency):
            f.seek(check_bytes * i, 0)
            enc_obj.update(f.read(check_once_bytes))
    return enc_obj.hexdigest()

# 检验下载文件是否完成
# download_path 本地文件  tontent_size  请求文件大小
def down_check(download_path, content_size):
    if not (os.path.exists(download_path)):
        print(f"{download_path} not exist".format(download_path))
        return

    print('开始校验文件完整性')
    file_count = os.stat(download_path).st_size
    time.sleep(3)
    if (file_count< content_size - 1024):
        os.remove(download_path)
        print("检验失败")

    else:
        print("检验结束")




if __name__ == '__main__':
    initial_file = '.\\files\\原文件.txt'
    modify_file = '.\\files\\被修改的文件.txt'
    md5_init = check_small_file(initial_file)
    md5_modify = check_small_file(modify_file)
    print(f'初始文件md5:{md5_init}\n修改后文件md5:{md5_modify}')
    # 尽管只多了一个字符串8,但是结果却完全不相同
    print(f'使用md5进行节选(大型文件)完整性校验获取的md5值:{check_big_file(initial_file)}')
    print(f'使用sha256进行节选(大型文件)完整性校验获取的sha256值:{check_big_file(initial_file, enc_type=hashlib.sha256())}')
