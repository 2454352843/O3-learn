import cv2
import numpy as np
import torch
from torchvision import transforms

from Pytorch.O3_estimate.utils import normalization

mean1= 0.30788937
std1 = 0.070841335
transform_BZ= transforms.Normalize(
    mean=[mean1 for i in range(3)],# 取决于数据集
    std=[std1 for i in range(3)]
)
train_tf = transforms.Compose([
                # transforms.Resize(self.img_size),
                # transforms.RandomHorizontalFlip(),#对图片进行随机的水平翻转
                # transforms.RandomVerticalFlip(),#随机的垂直翻转
                # transforms.ToTensor(),#把图片改为Tensor格式
                transform_BZ#图片标准化的步骤
            ])

def padding_black(img):  # 如果尺寸太小可以扩充
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


def tropomi():
    max = 0.056993544
    min = 0

    path = r'E:\data\5-mouth-dataset\Tropomi\2022_05_11\TropOMI_O3_PR_.tif'
    img = cv2.imread(path, -1)
    img =padding_black(img)
    data_normal = normalization(img, max, min)
    list = []
    for i in range(3):
        list.append(data_normal)
    list = np.array(list)
    data = torch.from_numpy(list)
    print(data.shape)

    data = train_tf(data.float())

    print(data.shape)




tropomi()
