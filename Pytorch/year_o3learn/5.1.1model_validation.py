
import torch
from torch.utils.data import DataLoader
from ST_Dataset import LoadData,WriteData
import torch.nn as nn
from torchvision.models import resnet18
from tqdm import tqdm

import os

import pandas as pd

from Pytorch.twice import models


def test(dataloader, model, device):
    pred_list = []
    # 将模型转为验证模式
    model.eval()
    # 测试时模型参数不用更新，所以no_gard()
    # 非训练， 推理期用到
    with torch.no_grad():
        # 加载数据加载器，得到里面的X（图片数据）和y(真实标签）
        for X, y in tqdm(dataloader):
            # 将数据转到GPU
            X, y = X.to(device), y.to(device)
            # 将图片传入到模型当中就，得到预测的值pred
            pred = model(X)
            re = pred[0].cpu().tolist()+y.cpu().tolist()
            pred_list.append(re)
        return pred_list


if __name__=='__main__':
    batch_size = 1

    # # 给训练集和测试集分别创建一个数据集加载器
    test_data = LoadData("Resource/test2.txt", True)
    test_dataloader = DataLoader(dataset=test_data, num_workers=4, pin_memory=True, batch_size=batch_size)

    # 如果显卡可用，则用显卡进行训练
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using {device} device")


    model = models.resnet18()
    model.load_state_dict(torch.load(r"D:\work\python\pycharm\O3-learn\Pytorch\year_o3learn\output\resnet18-big1\resnet18_no_pretrain_best.pth"))
    model.to(device)

    # 定义损失函数，计算相差多少，交叉熵，
    # loss_fn = nn.CrossEntropyLoss()

    '''
          获取结果
        '''
    # 获取模型输出
    pred_list = test(test_dataloader, model,device)
    print("pred_list = ", pred_list)



    df_pred = pd.DataFrame(data=pred_list, columns=['pred','label'])
    print(df_pred)
    df_pred.to_csv('pred_result_big1.csv', encoding='gbk', index=False)




