'''
2.2.2 生成数据加载器
'''
import config.log as log
import sys

import cv2
import torch
from PIL import Image
import numpy as np
import torchvision.transforms as transforms
from tqdm import tqdm
from utils import *
# 读取文件格式损坏自动跳过
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

from torch.utils.data import Dataset

logger = log.getLogger()
# 数据归一化与标准化
img_list = ['PS','T2M','TROPCOL_O3','U2M','V2M','ZPBL','cnc_O3','TropOMI_O3_PR','DEM','NDVI','POP','pri_sec']


mean1,std1,max1,min1 = get_math()

# transform_BZ= transforms.Normalize(
#     mean=mean,# 取决于数据集
#     std=std
# )
transform_BZ= transforms.Normalize(
    mean=[float(i) for i in mean1],# 取决于数据集
    std=[float(i) for i in std1]
)

class LoadData(Dataset):
    def __init__(self, txt_path, train_flag=True):
        self.imgs_info = self.get_images(txt_path)
        self.train_flag = train_flag
        self.img_size = (3540, 6158)

        self.train_tf = transforms.Compose([
                # transforms.Resize(self.img_size),
                # transforms.RandomHorizontalFlip(),#对图片进行随机的水平翻转
                # transforms.RandomVerticalFlip(),#随机的垂直翻转
                # transforms.ToTensor(),#把图片改为Tensor格式
                transform_BZ#图片标准化的步骤
            ])
        self.val_tf = transforms.Compose([##简单把图片压缩了变成Tensor模式
                # transforms.Resize(self.img_size),
                # transforms.ToTensor(),
                transform_BZ#标准化操作
            ])

    def get_images(self, txt_path):
        with open(txt_path, 'r', encoding='utf-8') as f:
            imgs_info = f.readlines()
            imgs_info = list(map(lambda x:x.strip().split('\t'), imgs_info))
        return imgs_info#返回图片信息

    def padding_black(self,img):  # 如果尺寸太小可以扩充
        w, h = img.shape
        x, y = self.img_size
        data = img
        if(w == 3541 and h == 6159):
            if (data[1, 0] < -10000):
                data = np.delete(data, 0, axis=1)
            else:
                data = np.delete(data, -1, axis=1)
            if (data[0, 1] < -10000):
                data = np.delete(data, 0, axis=0)
            else:
                data = np.delete(data, -1, axis=0)

        else:
            for i in range(w - x):
                data = np.delete(data, x - i, axis=0)

            for i in range(h - y):
                data = np.delete(data, y - i, axis=1)

        if (data.min()<-1000000):
            print('数据错误，最小值小于-100000')
            sys.exit()
        return data

    def __getitem__(self, index):#返回真正想返回的东西
        logger.info('getitem index:{n}'.format(n=index))
        value = self.imgs_info[index]
        item = Point(value)
        # print(item)

        sp = 0
        list = []
        for path in item.img_path:
            # print(path)
            img = cv2.imread(path,-1)
            img = self.padding_black(img)
            if (self.img_size != img.shape ):
                print('!!!!!!!!!!!---- 图片大小不一致 ---!!!!!!!!!!!!!!')
                sys.exit()
            list.append(img)

        # 归一化
        list1 = []
        for i in range(12):
            # print(i)
            data_normal = normalization(list[i], max1[i], min1[i])
            list1.append(data_normal)

        data = np.array(list1)
        data = torch.from_numpy(data)
        if self.train_flag:
            data = self.train_tf(data.float())
        else:
            data = self.val_tf(data.float())

        label = int(item.key)

        return data,label

    def __len__(self):
        return len(self.imgs_info)


def WriteData(fname, *args):
    with open(fname, 'a+') as f:
        for data in args:
            f.write(str(data)+"\t")
        f.write("\n")




class Point(object):
    def __init__(self,value):
        self.value = value

        self.lat = value[0]
        self.lon = value[1]
        self.data = value[2]
        self.time = value[3]
        self.key = value[4]

        self.img_path = value[5:-1]

        self.PS_path = value[5]
        self.T2M_path = value[6]
        self.GEOS_Oznone_path = value[7]
        self.U2M_path = value[8]
        self.V2M_path = value[9]
        self.ZPBL_path = value[10]
        self.SILAM_path = value[11]
        self.Tropomi_path = value[12]
        self.DEM_path = value[13]
        self.NDVI_path = value[14]
        # self.NDVI_resample_path = value[15]
        self.POP_path = value[15]
        self.pri_sec_path = value[16]
        self.tertiary_path = value[17]

    def __str__(self):
        return str(self.value)


if __name__ == "__main__":

    train_dataset = LoadData("Resource/t1.txt", True)
    print("数据个数：", len(train_dataset))
    train_loader = torch.utils.data.DataLoader(dataset=train_dataset,
                                               batch_size=10,
                                               shuffle=True)
    # for image, label in tqdm(train_loader):
    #     print("image.shape = ", image.shape)
    #     # print("image = ",image)
    #     print("label = ",label)

    for batch, (image, label) in enumerate(train_loader):  #
        print("image.shape = ", image.shape)
        # print("image = ",image)
        print("label = ", label)
