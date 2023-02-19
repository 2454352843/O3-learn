# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import random
import string

from config.log import getLogger
import numpy as np
logger = getLogger();



def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

# Press the green button in the gutter to run the script.

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

def reshape(data1,data2=0):
    a = 3
    b = 3
    data = np.zeros([3,3])
    size = data.shape
    for i in size[0]:
        for j in size[1]:
            data[i][j] = data1[i][j]
    print(data)



if __name__ == '__main__':
    # x= np.random.randint(1,20,size=(3,4))
    # y= np.random.randint(1,20,size=(3,4))
    # print(np.nan)
    # np.savetxt(r'.\resource\output\save_x.csv', x, fmt='%d', delimiter=',')
    a = np.array([3,6,9,12,18,24])
    b = a.reshape(2,3)

    reshape(b)