img_size = (3, 3)
ratio = 0.01
base_path = r'F:\data\dataset'
# 图片参数
lat_value = 3541
lon_value = 6159
# transform = (114, 0.01, 0.0, 40, 0.0, -0.01)
transform = (107, 0.01, 0.0, 45, 0.0, -0.01)
#华北平原地区
# 北纬(lat)32°～40°，东经(long)114°～121°  big:lon 107-124 lat 28-45
maxLat = 45
minLon = 107
lat_HB = 1700
lon_HB = 1700

# 读取文件顺序
tif_list = ['GEOS', 'LandCover', 'SILAM', 'Tropomi']
# GEOS_list = ['PS','T2M','TROPCOL_O3','U2M','V2M','ZPBL']
GEOS_list = ['PS', 'T2M', 'TROPCOL_O3', 'U2M', 'V2M', 'ZPBL']
LandCover = ['DEM', 'NDVI', 'POP', 'pri_sec']

# dataset
# 数据集位置顺序
arr_list = ['PS', 'T2M',  'U2M', 'V2M', 'ZPBL', 'SILAM', 'TropOMI', 'DEM', 'NDVI', 'POP', 'pri_sec']
batch_size = 128
# save_root = r'output/resnet18_StepLR/'
save_root = r'output/resnet18-big1/'
math_path_st = r'Resource/ST_math.txt'
math_arrName_ST = ['PS', 'T2M',  'U2M', 'V2M', 'ZPBL', 'SILAM', 'Tropomi', 'DEM', 'NDVI', 'POP', 'pri_sec','spatial','date','time']
math_arrName =['PS', 'T2M',  'U2M', 'V2M', 'ZPBL', 'SILAM', 'TropOMI', 'DEM', 'NDVI', 'POP', 'pri_sec']



# model
stride = 1
ch_in = 15
class_num = 1
epochs = 300

# 5.1
predict_loc = r'D:\work\python\pycharm\O3-learn\Pytorch\year_o3learn\pred_result_big1.csv'
predict_savepath = save_root

# 5.2
data_1_loc = 'output/resnet18_StepLR/resnet18_no_pretrain.txt'
data_2_loc = './output/resnet18/resnet18_no_pretrain.txt'
