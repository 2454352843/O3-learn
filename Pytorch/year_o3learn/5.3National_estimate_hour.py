import codecs
import datetime
import glob
import os
import time
import cv2
import gdal
import numpy as np
import pandas as pd
import torch
import PIL.Image as Image
from osgeo import osr
from torch.utils.data import DataLoader
from tqdm import tqdm

from Pytorch.year_o3learn import models
from Pytorch.year_o3learn.Resource import config
from Pytorch.year_o3learn.utils import Gdaltiff
from Utils.estimate_ST_Dataset import LoadData, WriteData

'''
估算全国范围的近地面臭氧浓度，并制作出tif图
输入： 指定的日期+小时
输出： tif
'''



class estimate:

    def __init__(self, date, time):
        self.date = date
        self.time = time
        self.ratio = config.ratio
        self.rows = config.lat_HB
        self.cols = config.lon_HB
        self.transform = config.transform
        self.temptxt = rf'Resource/temp_{date}_{time}.txt'
        self.folder = r'Resource/temp'
        self.base_path = config.base_path
        self.outdir = r'Resource/estimate'

        self.tif_list = self.get_tif()
        if self.tif_list == None:
            return

        self.get_datalist()
        self.get_folder()

    # 读取估算中需要使用的tif
    def get_tif(self):
        filesMap = {}
        tif_list = config.tif_list

        for dir in tif_list:
            map = {}
            # for root, dirs, files in os.walk(self.base_path + os.path.sep + i):
            #     list = []
            #     date = root.split(os.path.sep)[-1]
            #     for file_i in files:
            #         if 'tif' in file_i[-4:]:
            #             list.append(root + os.path.sep + file_i)
            #     map[date] = list
            #
            # # print(map)train_tf
            # 读取landcover
            if (dir == 'LandCover'):
                # 读取辅助数据
                other_files = glob.glob(self.base_path + os.path.sep + 'LandCover//*.tif')
                # 读取ndvi
                for root, dirs, files in os.walk(self.base_path + os.path.sep + 'LandCover//NDVI'):
                    if (len(files) == 0):
                        continue
                    list11 = []
                    date = root.split(os.path.sep)[-1]
                    for file_i in files:
                        if 'tif' in file_i[-4:]:
                            list11.append(root + os.path.sep + file_i)
                    map[date] = list11 + other_files

            else:  # 读取其他文件
                for root, dirs, files in os.walk(self.base_path + os.path.sep + dir):
                    if (len(files) == 0):
                        continue
                    list11 = []
                    date = root.split(os.path.sep)[-1]
                    for file_i in files:
                        if 'tif' in file_i[-4:]:
                            list11.append(root + os.path.sep + file_i)
                    map[date] = list11

            filesMap[dir] = map

        #  筛选读取改时间点对应的文件
        list_str = []
        date = self.date
        time = self.time
        if not date in filesMap['GEOS'].keys():
            return
        for k in filesMap['GEOS'][date]:
            if (time in k[-7:] and 'O3' not in k):
                # print(Timelist[j][:2])
                # print(k[-7:])
                list_str.append(k)

        if not date in filesMap['SILAM'].keys():
            return
        for k in filesMap['SILAM'][date]:
            if time in k[-6:]:
                list_str.append(k)

        if not date in filesMap['Tropomi'].keys():
            return
        for k in filesMap['Tropomi'][date]:
            if not 'temp' in k:
                list_str.append(k)

        # 筛选landcover
        dates = list((filesMap['LandCover']).keys())

        # 确定NDVI数据时间
        date_r = dates[0]
        for i in range(len(date_r) - 1):
            date_i = dates[i + 1]
            second_date = datetime.datetime.strptime(date_i, '%Y_%m_%d')
            first_date = datetime.datetime.strptime(date_r, '%Y_%m_%d')
            date_value = datetime.datetime.strptime(date, '%Y_%m_%d')
            date_r = date_r if abs(int((first_date - date_value).days)) < abs(
                int((second_date - date_value).days)) else date_i

        for k in filesMap['LandCover'][date_r]:
            if not 'temp' in k:
                list_str.append(k)

        # 如果缺少数据，则跳到下一条数据
        if len(list_str) < 11:
            list1 = []
            arr = config.arr_list
            for value in arr:
                mark = 0
                for i in list_str:
                    if value in i:
                        mark = 1
                        break
                if mark == 0:
                    list1.append(value)
            line = f"{date}_{time}  缺少{11 - len(list_str)}个数据,缺少的数据为：{list1}"
            print(line)
            return

        return list_str

    # 获取数据集
    def get_datalist(self):

        #  打开读取对应的文件
        tif_list = []
        arr_list = config.arr_list
        for i in range(len(arr_list)):
            for path in self.tif_list:
                if arr_list[i] in path:
                    tif_list.append(Gdaltiff(path))

        # print(len(tif_list))
        # 7. 生成数据集
        rows = tif_list[0].rows
        cols = tif_list[0].cols

        maxLat = config.maxLat
        minLon = config.minLon
        Lonlist = []
        Latlist = []
        print('构建经纬度队列')

        # 北纬(lat)32°～40°，东经(long)114°～121°  big:lon 107-124 lat 28-45
        for i in tqdm(range(config.lat_HB)):
            for j in range(config.lon_HB):
                lon = minLon + 0.01 * (j )
                lat = maxLat - 0.01 * (i )
                Lonlist.append(lon)
                Latlist.append(lat)

        # 构建经纬度列表
        print("构建数据集")
        data_list = []
        for j in tqdm(range(len(Latlist))):
            lat = str(round(Latlist[j], 2))
            lon = str(round(Lonlist[j], 2))
            point = {'lat': lat,
                     'lon': lon}
            # data = (lat if len(lat.split('.')[-1])>=2 else lat + '0') + '\t' +(lon if len(lon.split('.')[-1]) >= 2 else lon + '0') + '\t' + date + '\t' + Timelist[j] + '\t' + str(O3list[j])
            line = (lat if len(lat.split('.')[-1]) >= 2 else lat + '0') + '\t' + (
                lon if len(lon.split('.')[-1]) >= 2 else lon + '0') + '\t' + self.date + '\t' + self.time + '\t' + 'Ozone'
            for k in range(len(tif_list)):
                tif = tif_list[k]
                arr_value = tif.getImg(point)
                arr_value = np.reshape(arr_value, (1, config.img_size[0] * config.img_size[1])).tolist()
                line = line + '\t' + str(arr_value[0])
            line = line + '\n'
            data_list.append(line)

        with open(self.temptxt, 'w', encoding='UTF-8') as f:
            for line in data_list:
                f.write(str(line))
        return

    # 删除临时文件
    def remove_tmp(self):
        for root,folder,files in os.walk(self.folder):
            for file in files:
                filename = root+os.path.sep + file
                try:
                    os.remove(filename)
                except Exception as e:
                    print(e)


    def get_folder(self):
        # temp拆分 拆分为几个小的txt
        output_prefix = r'D:\work\python\pycharm\O3-learn\Pytorch\year_o3learn\Resource\temp'
        out_dir = output_prefix + os.path.sep +'temp_'+ self.date+'_'+self.time
        if not os.path.exists(output_prefix):
            os.makedirs(output_prefix)
        num_lines_per_file = 1000000
        # Open the input file in UTF-8 encoding
        with codecs.open(self.temptxt, 'r', encoding='utf-8') as f:
            # Create a counter for the current line number
            line_number = 1
            # Create a counter for the current output file numbert
            file_number = 1
            # Create an output file with the correct file number
            output_file = codecs.open(f'{out_dir}_{file_number}.txt', 'w', encoding='utf-8')
            print(f"\n构建第{file_number}个临时数据集")
            # Iterate over the lines in the input file
            for line in tqdm(f):
                # Write the line to the output file
                output_file.write(line)
                # Increment the line counter
                line_number += 1
                # If the line counter is greater than the number of lines per file,
                # close the output file, increment the file counter, and create a new output file
                if line_number > num_lines_per_file:
                    output_file.close()
                    file_number += 1
                    line_number = 1
                    print(f"\n构建第{file_number}个临时数据集")
                    output_file = codecs.open(f'{out_dir}_{file_number}.txt', 'w', encoding='utf-8')

            # Close the last output file
            output_file.close()
            # os.remove(self.temptxt)

    def get_dataset(self, i=0):
        for root, dirs, files in os.walk(self.folder):
            list3 = [n for n in filter(lambda x: 'txt' in x[-3:], files)]
            list3 = [n for n in filter(lambda x:  self.date+'_'+self.time in x, list3)]
            txts = [root + os.path.sep + txt for txt in list3]

        self.txt_len = len(txts)
        dataset = LoadData(txts[i])
        return dataset

    # 驱动主函数 进行预测
    def run(self):
        # 进行预测
        path = self.drive_estamite()

        # 根据预测结果作图
        self.draw(path)

    def draw(self, path):
        predict_data = pd.read_csv(path, encoding="GBK").sort_values('mark')  # ,index_col=0)

        predict_mark = [i * 1 for i in predict_data.to_numpy()[:, 1]]
        predict_pred = [i * 400 for i in predict_data.to_numpy()[:, 0]]

        add = (self.rows ) * (self.cols ) - len(predict_pred)
        data = np.array(predict_pred + [0 for i in range(add)]).reshape([self.rows, self.cols])
        data[data>400] = 0
        data[data<0] = 0
        print(f"\n最大值为:{data.max()}")
        print(f'最小值为:{data.min()}')
        # transform = (
        #     self.transform[0] + (2 * self.transform[1]), self.transform[1], self.transform[2],
        #     self.transform[3] + (self.transform[5] * 2), self.transform[4],
        #     self.transform[5])
        transform = self.transform

        self.writetif(data, transform)
        self.writejpg(data)


    #做出黑白图像(无地理信息)
    def writejpg(self,data):
        print('开始生成png')
        data[data >= 255] = 255
        a = np.array([data, data, data])

        rows = data.shape[0]
        cols = data.shape[1]
        image1 = Image.new("RGB", (rows, cols))
        for i in range(rows):
            for j in range(cols):
                image1.putpixel((i, j), (int(data[i, j]), int(data[i, j]), int(data[i, j])))

        # image1.show()
        save_path = self.outdir + os.path.sep + 'pred_result_{n}.png'.format(n=self.date + '_' + self.time)
        image1.save(save_path)

    def writetif(self,data, geotransform):
        print('开始生成tif')
        outname = self.outdir + os.path.sep + 'pred_result_{n}.tif'.format(n=self.date + '_' + self.time)
        nl, ns = [data.shape[0], data.shape[1]]

        bands = 1
        driver = gdal.GetDriverByName("GTiff")
        out_tif = driver.Create(outname, ns, nl, bands, gdal.GDT_Float64)
        out_tif.SetGeoTransform(geotransform)
        srs = osr.SpatialReference()
        srs.SetWellKnownGeogCS('WGS84')
        im_proj = srs.ExportToWkt()
        # proj_type = 'GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID["WGS 84",6378137,298.257223563,AUTHORITY["EPSG","7030"]],AUTHORITY["EPSG","6326"]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],AXIS["Latitude",NORTH],AXIS["Longitude",EAST],AUTHORITY["EPSG","4326"]]'
        out_tif.SetProjection(im_proj)  # 给新建图层赋予投影信息
        out_tif.GetRasterBand(1).WriteArray(data)
        del out_tif

    # 驱动估算主函数
    def drive_estamite(self):
        save_path = r'Resource/pred_result_{n}.csv'.format(n=self.date + '_' + self.time)
        if os.path.exists(save_path):
            return save_path
        batch_size = 32
        self.pred = [[], []]
        # # 给训练集和测试集分别创建一个数据集加载器
        self.get_dataset()
        for i in range(self.txt_len):
            test_data = self.get_dataset(i)
            test_dataloader = DataLoader(dataset=test_data, pin_memory=True, batch_size=batch_size)

            # 如果显卡可用，则用显卡进行训练
            device = "cuda" if torch.cuda.is_available() else "cpu"
            print(f"Using {device} device")

            model = models.resnet18()
            model.load_state_dict(torch.load(r"D:\work\python\pycharm\O3-learn\Pytorch\year_o3learn\output\resnet18-big\resnet18_no_pretrain_best.pth"))
            model.to(device)

            # 定义损失函数，计算相差多少，交叉熵，
            # loss_fn = nn.CrossEntropyLoss()
            '''
            获取结果
            '''
            # 获取模型输出
            pred_list = self.test(test_dataloader, model, device)
            # print("pred_list = ", pred_list)
            self.pred[0] += pred_list[0]
            self.pred[1] += pred_list[1]

        df_pred = pd.DataFrame({'pred': self.pred[0],
                                'mark': self.pred[1]})
        df_pred.to_csv(save_path, encoding='gbk', index=False)
        return save_path

    # 预测函数
    def test(self, dataloader, model, device):
        pred_list, mark_list = [], []
        # 将模型转为验证模式
        model.eval()
        # 测试时模型参数不用更新，所以no_gard()
        # 非训练， 推理期用到
        with torch.no_grad():
            # 加载数据加载器，得到里面的X（图片数据）和y(真实标签）
            for X, m in tqdm(dataloader):
                # 将数据转到GPU
                X = X.to(device)
                # 将图片传入到模型当中就，得到预测的值pred
                pred = model(X)
                re, me = pred.cpu().tolist(), m.tolist()

                for i in re:
                    pred_list += i

                mark_list += me
            return [pred_list, mark_list]

    def __str__(self):
        return f'{self.date}_{self.time}'

if __name__ == '__main__':
    time_start = time.time()
    date1 = '2022_05_01'
    time1 = '16'
    a = estimate(date1,time1)

    a.run()
    time_end = time.time()
    print(f"\ntrain time: {(time_end - time_start)}")
    # a.remove_tmp()