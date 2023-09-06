from sklearn.metrics import *  # pip install scikit-learn
import matplotlib.pyplot as plt  # pip install matplotlib
import pandas as pd  # pip install pandas
import os
import numpy as np
import statsmodels.api as sm
from Pytorch.year_o3learn.Resource import config
from Pytorch.year_o3learn.Utils.sandian import draw_scatter

predict_loc = config.predict_loc  # 3.ModelEvaluate.py生成的文件

predict_data = pd.read_csv(predict_loc, encoding="GBK")  # ,index_col=0)

predict_label = [i * 400 for i in predict_data.to_numpy()[:, 1]]
predict_pred = [i * 400 for i in predict_data.to_numpy()[:, 0]]



'''
    常用指标：r2，mae（平均绝对误差），mse(均方误差)，rmse
'''
list1 = []
r2 = r2_score(predict_label,predict_pred)
print(f'r2:{r2}')
list1.append(r2)

mae=mean_absolute_error(predict_label,predict_pred)
print(f'mae:{mae}')
list1.append(mae)

mse=mean_squared_error(predict_label,predict_pred)
print(f'mse:{mse}')
list1.append(mse)

rmse=np.sqrt(mse)
print(f'rmse:{rmse}')
list1.append(rmse)


# 写入文本
#  读出数据集为文本格式
# with open('Resource/train.txt', 'w', encoding='UTF-8') as f:
#     for train_img in list:
#         f.write(str(train_img))


'''
散点图
'''

# 求线性回归
X = sm.add_constant(predict_label)
y = predict_pred
result = sm.OLS(y,X).fit()
print(result.summary())

df = pd.DataFrame({'Observed': [int(i) - int(i) % 3 for i in predict_label],
                   'Estimated': [int(i) - int(i) % 3 for i in predict_pred],
                   'count': [1 for i in range(len(predict_pred))]
                   }
                  , columns=['Observed', 'Estimated', 'count'])

df1 = df.groupby(['Observed', 'Estimated']).agg({'count': lambda x: sum(list(x))
                                                 }).reset_index()

draw_scatter(df1,result,list1)
