'''
2.2.2 生成数据加载器
加入时空数据
'''
import time
import torch
import torchvision.transforms as transforms
import numpy as np

# 读取文件格式损坏自动跳过
from PIL import ImageFile


from Pytorch.year_o3learn.Utils.ST_utils import *
from Pytorch.year_o3learn.utils import get_math, normalization

ImageFile.LOAD_TRUNCATED_IMAGES = True
from torch.utils.data import Dataset


# 数据归一化与标准化
img_list = config.arr_list
# 分辨率
ratio = config.ratio
path = config.math_path_st

mean1, std1, max1, min1 = get_math(path)

# transform_BZ= transforms.Normalize(
#     mean=mean,# 取决于数据集
#     std=std
# )
transform_BZ = transforms.Normalize(
    mean=[float(i) for i in mean1],  # 取决于数据集
    std=[float(i) for i in std1]
)


class LoadData(Dataset):
    def __init__(self, txt_path, train_flag=True):
        self.imgs_info = self.get_images(txt_path)
        self.train_flag = train_flag
        self.img_size = config.img_size

        self.train_tf = transforms.Compose([
            # transforms.Resize(self.img_size),
            # transforms.RandomHorizontalFlip(),#对图片进行随机的水平翻转
            # transforms.RandomVerticalFlip(),#随机的垂直翻转
            # transforms.ToTensor(),#把图片改为Tensor格式
            transform_BZ  # 图片标准化的步骤
        ])
        self.val_tf = transforms.Compose([  ##简单把图片压缩了变成Tensor模式
            # transforms.Resize(self.img_size),
            # transforms.ToTensor(),
            transform_BZ  # 标准化操作
        ])

    def get_images(self, txt_path):
        with open(txt_path, 'r', encoding='utf-8') as f:
            imgs_info = f.readlines()
            imgs_info = list(map(lambda x: x.strip().split('\t'), imgs_info))
        return imgs_info  # 返回图片信息

    def __getitem__(self, index):  # 返回真正想返回的东西
        # logger.info('getitem index:{n}'.format(n=index))
        value = self.imgs_info[index]
        item = Point(value)
        # print(item)

        # 1 数据获取,清除异常值
        str1 = item.img_arr
        list = []
        for i in range(11):
            data = [float(i) for i in str1[i][1:-1].split(',')]
            list.append(data)

        # 2 时空数据获取
        # 华北平原地区
        # 北纬(lat)32°～40°，东经(long)114°～121°  big:lon 107-124 lat 28-45
        lat_value = int((45 - float(item.lat)) / ratio)
        lon_value = int((float(item.lon) - 107) / ratio)
        spatial_data = spatial_embedding(lat_value,lon_value)
        date_data = date_embedding(item.data)
        time_data = time_embedding(item.time)


        # 归一化
        list1 = []
        for i in range(11):
            # print(i)
            data_normal = normalization(np.array(list[i]).reshape(config.img_size[0], config.img_size[1]), max1[i],
                                        min1[i])
            list1.append(data_normal)

        list1.append(np.array(spatial_data))
        list1.append(np.array(date_data))
        list1.append(np.array(time_data))
        data = np.array(list1)
        data[data == np.nan] = 0
        data = torch.from_numpy(data).float()
        data = torch.where(torch.isnan(data), torch.full_like(data, 0), data)
        # 标准化
        data = self.train_tf(data)

        label = float(item.key)
        label = float(label / 400.0)
        return data, label

    def __len__(self):
        return len(self.imgs_info)


def WriteData(fname, *args):
    with open(fname, 'a+') as f:
        for data in args:
            f.write(str(data) + "\t")
        f.write("\n")


class Point(object):
    def __init__(self, value):
        self.value = value

        self.lat = value[0]
        self.lon = value[1]
        self.data = value[2]
        self.time = value[3]
        self.key = value[4]

        self.img_arr = value[5:]

        # self.PS_path = value[5]
        # self.T2M_path = value[6]
        # self.GEOS_Oznone_path = value[7]
        # self.U2M_path = value[8]
        # self.V2M_path = value[9]
        # self.ZPBL_path = value[10]
        # self.SILAM_path = value[11]
        # self.Tropomi_path = value[12]
        # self.DEM_path = value[13]
        # self.NDVI_path = value[14]
        # # self.NDVI_resample_path = value[15]
        # self.POP_path = value[15]
        # self.pri_sec_path = value[16]
        # self.tertiary_path = value[17]

    def __str__(self):
        return str(self.value)


if __name__ == "__main__":

    train_dataset = LoadData("Resource/train.txt", True)
    print("数据个数：", len(train_dataset))
    train_loader = torch.utils.data.DataLoader(dataset=train_dataset,
                                               batch_size=10,
                                               shuffle=True)

    time_start = time.time()
    for batch, (image, label) in enumerate(train_loader):
        time_end = time.time()
        print(f"train time: {(time_end - time_start)}")
        time_start = time_end
        print(image.max())
        print(image.min())
        # print("image = ",image)
        print("label = ", label)
