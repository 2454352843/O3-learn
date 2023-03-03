img_size = (3,3)
ratio = 0.01
base_path = r'E:\data\5-mouth-dataset'

#读取文件顺序
tif_list = ['GEOS', 'LandCover', 'SILAM', 'Tropomi']
GEOS_list = ['PS','T2M','TROPCOL','U2M','V2M','ZPBL']
LandCover = ['DEM','NDVI','POP','pri_sec','tertiary']

# 数据集位置顺序
arr_list = ['PS', 'T2M', 'TROPCOL_O3', 'U2M', 'V2M', 'ZPBL', 'cnc_O3', 'TropOMI_O3_PR', 'DEM', 'NDVI', 'POP', 'pri_sec']

batch_size = 128