import torch
from cv2 import imread
from torchvision.transforms import transforms
import numpy as np
from Pytorch.O3_estimate.utils import get_math, normalization

img_list = ['PS','T2M','TROPCOL_O3','U2M','V2M','ZPBL','cnc_O3','TropOMI_O3_PR','DEM','NDVI','POP','pri_sec']


mean1,std1,max1,min1 = get_math()

transform_BZ= transforms.Normalize(
    mean=[float(i) for i in mean1],# 取决于数据集
    std=[float(i) for i in std1]
)
transform1 = transforms.Compose([
    transforms.Normalize(mean=[0,0,0,0,0], std=[255,255,255,255,255])
    ])
train_tf = transforms.Compose([
                # transforms.Resize(self.img_size),
                # transforms.RandomHorizontalFlip(),#对图片进行随机的水平翻转
                # transforms.RandomVerticalFlip(),#随机的垂直翻转
                # transforms.ToTensor(),#把图片改为Tensor格式
                transform_BZ#图片标准化的步骤
            ])

path1 = r'../Resource/t1.txt'


def padding_black( img):  # 如果尺寸太小可以扩充
    w, h = img.shape
    x, y = (3540, 6158)
    data = img
    if (w == 3541 and h == 6159):
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

    if (data.min() < -1000000):
        print('数据错误，最小值小于-100000')

    return data

with open(path1, 'r', encoding='utf-8') as f:
    imgs_info = f.readlines()
    imgs_info = list(map(lambda x: x.strip().split('\t'), imgs_info))


info = [i[5:] for i in imgs_info]

sp = 0
list = []
for path in info[1][:-1]:
    print(path)
    img = imread(path, -1)
    data1 = padding_black(img)



    list.append(data1)

list1 = []
for i in range(12):
    print(i)
    data_normal = normalization(list[i],max1[i],min1[i])
    list1.append(data_normal)


data = np.array(list1)
# C = torch.from_numpy(B)

data = torch.from_numpy(data)
img1 = train_tf(data.float())

print(data.shape)

