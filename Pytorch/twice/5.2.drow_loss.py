# -*-coding:utf-8-*-
from matplotlib import pyplot as plt
import numpy as np

from Pytorch.twice.Resource import config


def ReadData(data_loc):
    epoch_list = []
    train_loss_list = []
    test_loss_list = []
    test_accuracy_list = []

    # open(data_loc,"r").readlines()
    with open(data_loc, "r") as f:
        linedata = f.readlines()

        for line_i in linedata:
            data = line_i.split('\t')
            print("data = ", data)
            epoch_i , train_loss_i,test_loss_i,test_accuracy_i =data[1], data[3],data[5],data[7]
            epoch_list.append(int(epoch_i))
            train_loss_list.append(float(train_loss_i))
            test_loss_list.append(float(test_loss_i))
            test_accuracy_list.append(float(test_accuracy_i))

    # print(epoch_list)
    # print(train_loss_list)
    # print(test_loss_list)
    # print(test_accuracy_list)
    return epoch_list, train_loss_list  ,test_loss_list,test_accuracy_list



def DrawLoss(train_loss_list,train_loss_list_2):
    plt.style.use('dark_background')
    plt.title("Loss")
    plt.xlabel("epoch")
    plt.ylabel("loss")

    train_loss_list = train_loss_list[:10]
    train_loss_list_2 = train_loss_list_2[:10]

    epoch_list = [i for i in range(len(train_loss_list))]

    p1, = plt.plot(epoch_list, train_loss_list, linewidth=3)
    p2, = plt.plot(epoch_list, train_loss_list_2, linewidth=3)

    plt.legend([p1, p2], ["with pretrain", "no pretrain"])
    plt.show()

def DrawAcc(train_loss_list,train_loss_list_2):
    plt.style.use('dark_background')
    plt.title("Accuracy")
    plt.xlabel("epoch")
    plt.ylabel("accuracy")

    train_loss_list = train_loss_list[:10]

    epoch_list = [i for i in range(len(train_loss_list))]

    p1, = plt.plot(epoch_list, train_loss_list, linewidth=3)
    p2, = plt.plot(epoch_list, train_loss_list_2, linewidth=3)

    plt.legend([p1, p2], ["with transfer", "no transfer"])
    plt.show()

if __name__ == '__main__':
    data_1_loc =config.data_1_loc
    data_2_loc = config.data_2_loc

    _, train_loss_list  ,test_loss_list,test_accuracy_list = ReadData(data_1_loc)
    _, train_loss_list_2  ,test_loss_list_2,test_accuracy_list_2 = ReadData(data_2_loc)

    DrawLoss(train_loss_list,train_loss_list_2)

   # DrawAcc(test_accuracy_list,test_accuracy_list_2)
