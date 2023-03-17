from sklearn.metrics import *  # pip install scikit-learn
import matplotlib.pyplot as plt  # pip install matplotlib
import pandas as pd  # pip install pandas
import os
import numpy as np

from Pytorch.twice.Resource import config
from Pytorch.twice.utils.sandian import draw_scatter

predict_loc = config.predict_loc  # 3.ModelEvaluate.py生成的文件

predict_data = pd.read_csv(predict_loc, encoding="GBK")  # ,index_col=0)

predict_label = [i * 300 for i in predict_data.to_numpy()[:, 1]]
predict_pred = [i * 300 for i in predict_data.to_numpy()[:, 0]]

# '''
#     常用指标：r2，mae（平均绝对误差），mse(均方误差)，rmse
# '''
# list = []
# r2 = r2_score(predict_label,predict_pred)
# print(f'r2:{r2}')
# list.append(f'r2: {r2}')
#
# mae=mean_absolute_error(predict_label,predict_pred)
# print(f'mae:{mae}')
# list.append(f'mae: {mae}')
#
# mse=mean_squared_error(predict_label,predict_pred)
# print(f'mse:{mse}')
# list.append(f'mse: {mse}')
#
# rmse=np.sqrt(mse)
# print(f'rmse:{rmse}')
# list.append(f'rmse: {rmse}')
#
#
# # 写入文本
# #  读出数据集为文本格式
# with open('Resource/train.txt', 'w', encoding='UTF-8') as f:
#     for train_img in list:
#         f.write(str(train_img))
#
#
# '''
# 散点图
# '''
df = pd.DataFrame({'Observed': [int(i) for i in predict_label],
                   'Estimated': [int(i) for i in predict_pred],
                   }
                  , columns=['Observed', 'Estimated'])

g = df.groupby('Observed')
df1 = g['Estimated'].value_counts()
draw_scatter(df1)
# a = df.groupby(['pred','label']).agg({'水果': [', '.join], '数量': lambda x: list(x),
#                         '重量': lambda x: list(x)}).reset_index()
