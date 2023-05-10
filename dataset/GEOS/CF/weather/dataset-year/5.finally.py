import os,shutil
import glob
import datetime

from tqdm import tqdm

'''
1.构建数据集结构文件夹
2.与气象结果合并
'''

input_folder = r'F:\data\xyz-O3\GEOS-CF\workspace\weather\4resample'
output_path = r'F:\data\xyz-O3\GEOS-CF\workspace\weather\5finally'


def get_folder(tif):
    path, basename = os.path.split(tif)

    date = basename.split('_')[1]
    year,mouth,day = date[:4],date[4:6],date[6:8]
    time =basename.split('_')[2]
    value = basename.split('_')[3].split('.')[0]
    out_dir = output_path + os.path.sep + f'{year}_{mouth}_{day}'

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)


    os.rename(tif,out_dir+os.path.sep + f'{value}_{time}.tif')

def delete_trop(tif):
    path, basename = os.path.split(tif)

    if('TropOMI' in tif):
        new_name = basename[8:]
        out_name = path + os.path.sep +new_name


        os.rename(tif,out_name)

#1。 数据集构建
def main():
    for root,dir,files in  os.walk(output_path):


        for i in files:
            if ('tif' in i):
                delete_trop(root+'//'+i)

#2.检查缺失
def main1():
    pass

if __name__ == '__main__':
    main()
