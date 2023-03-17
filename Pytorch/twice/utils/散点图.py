import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('C:\\Users\\ZXS\\Desktop\\专利\\NO2.csv')
data[u'prediction'][(data[u'prediction']<0) | (data[u'prediction']>150)] = None
data[u'observe'][(data[u'observe']>150) | (data[u'observe']<0)] = None
df = pd.DataFrame(data)
df.plot.scatter('observe', 'prediction', s=1, c='count', colormap='jet')
# fig, ax = plt.subplots(1, 1,figsize=(7,7),dpi=300)
# ax.scatter('test_Y', 'predictions', s=1)
# ax.plot((0, 1), (0, 1), transform=ax.transAxes, ls='--',c='k', label="1:1 line")
#定义x
x = [0,150]
#定义y
y = x
#绘制
plt.plot(x,y,'--',color='black')
# plt.title('PM10')
plt.savefig('C:\\Users\\ZXS\\Desktop\\专利\\NO2_scatter.png')
plt.show()