img_size = (3, 3)
ratio = 0.01
base_path = r'E:\data\5-mouth-dataset'
# 图片参数
lat_value = 3541
lon_value = 6159
transform = (73.5, 0.01, 0.0, 53.57000000000001, 0.0, -0.01)

# 读取文件顺序
tif_list = ['GEOS', 'LandCover', 'SILAM', 'Tropomi']
# GEOS_list = ['PS','T2M','TROPCOL_O3','U2M','V2M','ZPBL']
GEOS_list = ['PS', 'T2M', 'TROPCOL_O3', 'U2M', 'V2M', 'ZPBL']
LandCover = ['DEM', 'NDVI', 'POP', 'pri_sec']

# dataset
# 数据集位置顺序
arr_list = ['PS', 'T2M', 'TROPCOL_O3', 'U2M', 'V2M', 'ZPBL', 'cnc_O3', 'TropOMI_O3_PR', 'DEM', 'NDVI', 'POP', 'pri_sec']
batch_size = 128
# save_root = r'output/resnet18_StepLR/'
save_root = r'output/resnet18-bt/'
math_path_st = r'Resource/math_ST.txt'
math_path_st = r'Resource/math_ST.txt'
math_arrName_ST = ['PS', 'T2M', 'TROPCOL_O3', 'U2M', 'V2M', 'ZPBL', 'SILAM', 'Tropomi', 'DEM', 'NDVI', 'POP', 'pri_sec','spatial','date','time']
math_arrName = ['PS', 'T2M', 'TROPCOL_O3', 'U2M', 'V2M', 'ZPBL', 'SILAM', 'Tropomi', 'DEM', 'NDVI', 'POP', 'pri_sec']



# model
stride = 1
ch_in = 15
class_num = 1
epochs = 300

# 5.1
predict_loc = r'./pred_result32.csv'
predict_savepath = save_root

# 5.2
data_1_loc = 'output/resnet18_StepLR/resnet18_no_pretrain.txt'
data_2_loc = './output/resnet18/resnet18_no_pretrain.txt'
