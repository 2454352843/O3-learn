import glob
import os, shutil
import datetime
from tqdm import tqdm

'''
1.构建数据集
2.检查缺失
'''

input_folder = r'F:\data\xyz-O3\S5P\workspace\workspace-20230301-230401\9clip'
output_path = r'F:\data\xyz-O3\S5P\workspace\workspace-20230301-230401\10finally'


def get_folder(tif):
    path, basename = os.path.split(tif)
    short_name, extension = os.path.splitext(basename)
    if ('202' in short_name):
        i = short_name.find('2022')
        if(i<0):
            i = short_name.find('2023')
        date = short_name[i:i + 8]
        date = datetime.datetime.strptime(date, '%Y%m%d').strftime('%Y_%m_%d')
        print(date)
        out_dir = output_path + os.path.sep + date

        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        else:
            print(f'{tif} exist')
            return

        os.rename(tif,out_dir+os.path.sep + 'TropOMI_O3.tif')

    else:
        print(f'{tif} error')


#1。 数据集构建
def main():
    tifs = glob.glob(input_folder + os.path.sep + '*.tif')

    for i in (range(len(tifs))):
        tif = tifs[i]
        get_folder(tif)

#2.检查缺失
def main1():
    pass

if __name__ == '__main__':
    main()
