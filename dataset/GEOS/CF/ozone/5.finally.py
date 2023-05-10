import os,shutil
import glob
import datetime

from tqdm import tqdm

'''
1.构建数据集结构文件夹
2.与气象结果合并
'''

input_folder = r'F:\data\xyz-O3\GEOS-CF\workspace\ozone\4resample'
output_path = r'F:\data\xyz-O3\GEOS-CF\workspace\ozone\5finally'


def get_folder(tif):
    path, basename = os.path.split(tif)

    date = basename.split('+')[-1]
    year,mouth,day = date[:4],date[4:6],date[6:8]
    time = date[9:11]
    out_dir = output_path + os.path.sep + f'{year}_{mouth}_{day}'

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)


    os.rename(tif,out_dir+os.path.sep + f'TropOMI_O3_{time}.tif')




#1。 数据集构建
def main():
    tifs = glob.glob(input_folder + os.path.sep + '*.tif')

    for i in tqdm(range(len(tifs))):
        tif = tifs[i]
        get_folder(tif)

#2.检查缺失
def main1():
    pass

if __name__ == '__main__':
    main()
