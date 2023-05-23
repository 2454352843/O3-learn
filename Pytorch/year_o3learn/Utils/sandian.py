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
from mpl_toolkits import axes_grid1

def add_colorbar(im, aspect=20, pad_fraction=0.5, **kwargs):
    """Add a vertical color bar to an image plot."""
    divider = axes_grid1.make_axes_locatable(im.axes)
    width = axes_grid1.axes_size.AxesY(im.axes, aspect=1./aspect)
    pad = axes_grid1.axes_size.Fraction(pad_fraction, width)
    current_ax = plt.gca()
    cax = divider.append_axes("right", size=width, pad=pad)
    plt.sca(current_ax)
    return im.axes.figure.colorbar(im, cax=cax, **kwargs)

def draw_scatter(df, result,list):
    df = df.drop(df[(df.Observed <= 1)].index)
    df = df.drop(df[(df.Estimated <= 1)].index)
    # df = df.drop(df[(df.Observed >= 300)].index)
    n = df[(df.Observed - df.Estimated >= 150)].index
    df = df.drop(n)

    print(f'异常值：{len(n)}')

    fig = plt.figure()
    ax = fig.gca()

    norm = mpl.colors.Normalize(vmin=0, vmax=300)  # 规定colorbar尺寸
    # cmp = mpl.colors.ListedColormap(["green", "orange",
    #                                  "gold", "blue", "k",
    #                                  "#550011", "purple",
    #                                  "red"])
    # norm = mpl.colors.BoundaryNorm([0, 1, 2, 5, 10, 20, 30, 50],cmp.N)

    # plt.scatter(df['observe'], df['prediction'], c=df['num'],colormap='jet')
    im = ax.scatter(x=df['Observed'], y=df['Estimated'], c=df['count'], s=7, cmap='jet', alpha=0.7, norm=norm)
    ax.plot((0, 1), (0, 1), transform=ax.transAxes, ls='--', c='black')

    # 画线性回归线
    x = np.linspace(0, 400)
    plt.plot(x, result.params[0] + result.params[1] * x, c='black', lw=2)

    plt.title('ResNet-18', fontsize =15)


    # 所有文本使用统一的样式

    styles = {"size": 15, "color": "black", 'linespacing': 1.3, 'weight': 'light'}
    # ax.legend(['R2: 0.694'])  ## 添加图例。数组里面的第一个图表示画的第一条曲线的图例
    ax.text(15, 250,
            f'N = 129457\ny = {round(result.params[1], 2)}x+{round(result.params[0], 2)}\nMAE = {round(list[1],3)}\nR$^{2}$ ={round(list[0],3)} \nRMSE = {round(list[3],3)}',
            ha='left', **styles)
    ax.text(310, 10, 'Hourly', ha='left', **styles)

    # colorbar
    cb1 = add_colorbar(im)
    # cb1 = plt.colorbar(im, fraction=0.03, pad=0.05)
    cb1.ax.tick_params(labelsize=12)
    tick_locator = ticker.MaxNLocator(nbins=5)  # colorbar上的刻度值个数
    cb1.locator = tick_locator
    cb1.set_ticks([50 * (i + 1) for i in range(6)])
    cb1.set_label('Count', size=13)
    # cb1.set_label(label='Points', rotation='horizontal', loc='top')  # loc参数


    # 设置label
    leg = ax.legend(loc='best', fontsize=24)
    leg.get_frame().set_alpha(0.0)
    fm = mpl.font_manager.FontProperties()
    fm.set_size(20)  # 设置字体为20，默认是10
    ax.set_xlabel('Observed(ug/m$^3$)', size=15, fontproperties=fm)
    ax.set_ylabel('Estimated(ug/m$^3$)', size=15)
    ax.tick_params(labelsize=24)
    plt.subplots_adjust(wspace=11.6, hspace=0.6, left=0.15, bottom=0.15, right=0.88, top=0.90)

    x = np.arange(0, 450, 50)
    y = np.arange(0, 450, 50)
    plt.xticks(x)
    plt.yticks(y)
    plt.xlim(0.0, 400)
    plt.ylim(0.0, 400)
    plt.tick_params(labelsize=15)
    labels = ax.get_xticklabels() + ax.get_yticklabels()
    [label.set_fontname('Times New Roman') for label in labels]
    # x=[0,50]
    # y=x
    # plt.plot(x,y,ls='--',lw=2,c='black')

    plt.savefig('./scatterDiagram32.png')
    plt.show()
