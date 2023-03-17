# _*_ coding:utf-8 _*_
# @功能描述：todo
# @程序作者：potato张
# @版权信息：15993617315@163.com
# @版本号：python 3.8.2

import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import ticker
import numpy as np

def draw_scatter(df):
    df = df.drop(df[(df.Observed <= 0)].index)
    df = df.drop(df[(df.Estimated <= 0)].index)

    fig = plt.figure()
    ax = fig.gca()
    # plt.scatter(df['observe'], df['prediction'], c=df['num'],colormap='jet')
    im = ax.scatter(x=df['Observed'], y=df['Estimated'], c='b', s=2, cmap='jet')
    ax.plot((0, 1), (0, 1), transform=ax.transAxes, ls='--', c='black')
    ax.title.set_text('SanDianTu')
    ax.set_xlabel('Observed')
    ax.set_ylabel('Estimated')
    # ax.legend(['R2: 0.694']) ## 添加图例。数组里面的第一个图表示画的第一条曲线的图例
    ax.text(5, 320, 'R2: 0.694',bbox=dict(facecolor='red', alpha=0.5))

    # colorbar
    # cb1 = plt.colorbar(im, fraction=0.03, pad=0.05)
    # cb1.ax.tick_params(labelsize=12)
    # tick_locator = ticker.MaxNLocator(nbins=5)  # colorbar上的刻度值个数
    # cb1.locator = tick_locator
    # cb1.set_ticks([10,20,30,40,50,60])
    # cb1.set_label('Points')
    # plt.xlabel('Observe')
    # plt.ylabel('Prediction')

    x = np.arange(0, 400, 50)
    y = np.arange(0, 400, 50)
    plt.xticks(x)
    plt.yticks(y)
    plt.tick_params(labelsize=10)
    labels = ax.get_xticklabels() + ax.get_yticklabels()
    [label.set_fontname('Times New Roman') for label in labels]
    # x=[0,50]
    # y=x
    # plt.plot(x,y,ls='--',lw=2,c='black')
    # plt.savefig('scatterDiagram.png')
    plt.show()
