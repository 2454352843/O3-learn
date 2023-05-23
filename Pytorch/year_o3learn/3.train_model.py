import sys
import time

import numpy
import torch
from torch import nn
from torch.utils.data import DataLoader
from Dataset import LoadData,WriteData

from Pytorch.twice import models
from Pytorch.twice.Resource import config

torch.cuda.max_split_size_mb = 128

def train(dataloader, model, loss_fn, optimizer,device):
    size = len(dataloader.dataset)
    avg_loss = 0
    # 从数据加载器中读取batch（一次读取多少张，即批次数），X(图片数据)，y（图片真实标签）。
    for batch, (X, y) in enumerate(dataloader):#固定格式：batch：第几批数据，不是批次大小，（X，y）：数值用括号


        # train_dataset = LoadData("Resource/train.txt", True)
        # X,y = train_dataset[813102]
        # y = torch.from_numpy(numpy.array(y))
        # 将数据存到显卡

        # y = y.reshape(y.size(),1)

        y = y.view(y.size()[0],1)
        X, y = X.to(device), y.to(device)
        # 得到预测的结果pred

        pred = model(X)
        if(torch.isnan(pred).any()):
            print("pred is nan ")
            sys.exit()
        loss = loss_fn(pred, y)
        avg_loss += loss
        # 反向传播，更新模型参数
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        # 每训练10次，输出一次当前信息
        if batch % 100 == 0:
            loss, current = loss.item(), batch * len(X)
            print(f"loss: {loss:>7f}  [{current:>5d}/{size:>5d}]")

    # 当一个epoch完了后返回平均 loss
    avg_loss /= size
    avg_loss = avg_loss.detach().cpu().numpy()
    return avg_loss


def validate(dataloader, model, loss_fn, device):
    size = len(dataloader.dataset)
    # 将模型转为验证模式
    model.eval()
    # 初始化test_loss 和 correct， 用来统计每次的误差
    test_loss, correct = 0, 0
    # 测试时模型参数不用更新，所以no_gard()
    # 非训练， 推理期用到
    with torch.no_grad():
        # 加载数据加载器，得到里面的X（图片数据）和y(真实标签）
        for X, y in dataloader:
            # 将数据转到GPU
            X, y = X.to(device), y.to(device)
            # 将图片传入到模型当中就，得到预测的值pred
            pred = model(X)
            # 计算预测值pred和真实值y的差距
            test_loss += loss_fn(pred, y).item()
            # 统计预测正确的个数(针对分类)
            correct += (pred.argmax(1) == y).type(torch.float).sum().item()
    test_loss /= size
    correct /= size
    print(f"correct = {correct}, Test Error: \n Accuracy: {(100 * correct):>0.1f}%, Avg loss: {test_loss:>8f} \n")
    return correct, test_loss


if __name__=='__main__':
    batch_size = config.batch_size
    # batch_size = 128

    # # 给训练集和测试集分别创建一个数据集加载器
    train_data = LoadData("Resource/train.txt", True)
    valid_data = LoadData("Resource/test.txt", False)

    #num_workers 线程数 pin_memory 数据存到内存中  shuffle 是否打乱顺序
    # train_dataloader = DataLoader(dataset=train_data, num_workers=4, pin_memory=True, batch_size=batch_size, shuffle=True)
    train_dataloader = DataLoader(dataset=train_data,  pin_memory=True, batch_size=batch_size, shuffle=True)
    valid_dataloader = DataLoader(dataset=valid_data, num_workers=4, pin_memory=True, batch_size=batch_size)

    # 如果显卡可用，则用显卡进行训练
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using {device} device")


    model = models.resnet18()
    print(model)
    model = model.to(device)

    # 定义损失函数，计算相差多少，交叉熵，
    loss_fn = nn.L1Loss()
    loss_fn=loss_fn.to(device)

    # 定义优化器，用来训练时候优化模型参数，随机梯度下降法
    learning_rate = 1e-3
    optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)

    epochs = 50
    loss_ = 10
    save_root = config.save_root


    for t in range(epochs):
        print(f"Epoch {t + 1}\n-------------------------------")
        time_start = time.time()
        avg_loss = train(train_dataloader, model, loss_fn, optimizer, device)
        time_end = time.time()
        print(f"train time: {(time_end - time_start)}")
        # (dataloader, model, loss_fn, device)jif
        val_accuracy, val_loss = validate(valid_dataloader, model,loss_fn, device)
        # 写入数据
        WriteData(save_root + "resnet18_no_pretrain.txt",
                  "epoch", t,
                  "train_loss", avg_loss,
                  "val_loss", val_loss,
                  "val_accuracy", val_accuracy)
        if t % 5 == 0:
            torch.save(model.state_dict(), save_root + "resnet18_no_pretrain_epoch" + str(t) + "_loss_" + str(avg_loss) + ".pth")

        torch.save(model.state_dict(), save_root + "resnet18_no_pretrain_last.pth")

        if avg_loss < loss_:
            loss_ = avg_loss
            torch.save(model.state_dict(), save_root + "resnet18_no_pretrain_best.pth")

