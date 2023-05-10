import os, shutil

from tqdm import tqdm

'''
整理老师给的文件
1.修改文件夹格式
'''
input_path = r'F:\data\xyz-O3\GEOS-CF\processed'
output_path = r'F:\data\xyz-O3\GEOS-CF\dataset'


def get_folder(tif):
    path, basename = os.path.split(tif)

    date = path.split(os.path.sep)[-2]
    time = path.split(os.path.sep)[-1]
    out_dir = output_path + os.path.sep + f'{date}'

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    new_name = out_dir + os.path.sep + f"{basename.split('.')[0]}_{time}.tif"
    os.rename(tif, new_name)


def main():
    tif_list = []
    for root, dirs, files in os.walk(input_path):
        for file in files:
            if ('tif' in file):
                tif_list.append(root + os.path.sep + file)

    for i in tqdm(range(len(tif_list))):
        tif = tif_list[i]
        get_folder(tif)


if __name__ == '__main__':
    main()
