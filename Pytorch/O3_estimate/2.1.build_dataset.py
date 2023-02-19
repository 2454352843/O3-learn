import os
import random
import pandas as pd
import glob
from tqdm import tqdm

train_ratio = 0.9
test_ratio = 1 - train_ratio

rootdata = r"E:\data\5-mouth-dataset"
tif_list = ['GEOS', 'LandCover', 'SILAM', 'Tropomi']

data_list, train_list, test_list = [], [], []
len_list = 0

def get_tiflist(dir):
    map = {}
    for root, dirs, files in os.walk(rootdata + os.path.sep + dir):
        list = []
        date = root.split(os.path.sep)[-1]
        for file_i in files:
            if 'tif' in file_i[-4:]:
                list.append(root + os.path.sep + file_i)
        map[date] = list

    # print(map)train_tf
    map.pop(dir)
    return map

# 构建测试集、训练集
def main():

    xlsxfiles = glob.glob(rootdata + os.path.sep + 'Site-xlsx' + os.path.sep + "*.xlsx")
    global len_list

   # 1.获取全部数据
    filesMap = {}
    for i in tif_list:
        filesMap[i] = get_tiflist(i)

    # print(filesMap)
    data_list = []

    # 2.根据日期读取数据
    for i in tqdm(range(len(xlsxfiles))):
        xlsxfile = xlsxfiles[i]
        # print(xlsxfile.split(os.path.sep)[-1])
        date = xlsxfile.split(os.path.sep)[-1][:-5].replace('-', '_')
        df = pd.read_excel(xlsxfile)


        Latlist = df.values[:, 1]
        Lonlist = df.values[:, 2]
        O3list = df.values[:, 6]

        Timelist = df.values[:, 5]
        Timelist = [i[:2] for i in Timelist]
        len_list = len_list + int(len(O3list))

        for j in range(len(Latlist)):
            list_str = []
            for k in filesMap['GEOS'][date]:
                if Timelist[j][:2] in k[-7:] :
                    # print(Timelist[j][:2])
                    # print(k[-7:])
                    list_str.append(k)

            for k in filesMap['SILAM'][date]:
                if Timelist[j][:2] in k[-6:] :
                    list_str.append(k)

            for k in filesMap['Tropomi'][date]:
                if not 'temp' in k :
                 list_str.append(k)


            if int(date[-2:]) <= 17:

                for k in filesMap['LandCover'][date[:-2]+'09']:
                    if ('resample' in k):
                        continue
                    list_str.append(k)
            else:
                for k in filesMap['LandCover'][date[:-2]+'25']:
                    if ('resample' in k):
                        continue
                    list_str.append(k)

            lat = str(round(Latlist[j], 2))
            lon =  str(round(Lonlist[j], 2))

            data = (lat if len(lat.split('.')[-1])>=2 else lat + '0') + '\t' +(lon if len(lon.split('.')[-1]) >= 2 else lon + '0') + '\t' + date + '\t' + Timelist[j] + '\t' + str(O3list[j])

            for k in list_str:
                data = data + '\t' + k

            # print(data)
            data_list.append(data + '\n')

        # print(date_list)


    #  构建测试集 训练集
    random.shuffle(data_list)
    for i in range(0, int(len(data_list) * train_ratio)):

        train_list.append(data_list[i])

    for i in range(int(len(data_list) * train_ratio), len(data_list)):

        test_list.append(data_list[i])





    with open('Resource/train.txt', 'w', encoding='UTF-8') as f:
        for train_img in train_list:
            f.write(str(train_img))

    with open('Resource/test.txt', 'w', encoding='UTF-8') as f:
        for test_img in test_list:
            f.write(test_img)


if __name__ == '__main__':
    main()
    print("共有 {n} 条数据".format(n = len_list))

