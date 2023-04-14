#数据集超参n
n = 3
img_size = (n,n)
ratio = 0.01
base_path = r'E:\data\5-mouth-dataset'

#文件栅格信息
tif_x,tif_y = 6159, 3541

#读取文件顺序
tif_list = ['GEOS', 'LandCover', 'SILAM', 'Tropomi']
# GEOS_list = ['PS','T2M','TROPCOL_O3','U2M','V2M','ZPBL']
GEOS_list = ['PS','T2M','TROPCOL_O3','U2M','V2M','ZPBL']
LandCover = ['DEM','NDVI','POP','pri_sec']

# ST
math_path_st = r'Resource/math_ST.txt'
# 数据集位置顺序

arr_list = ['PS', 'T2M', 'TROPCOL_O3', 'U2M', 'V2M', 'ZPBL', 'cnc_O3', 'TropOMI_O3_PR', 'DEM', 'NDVI', 'POP', 'pri_sec']

batch_size = 128