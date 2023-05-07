# -*- coding: utf-8 -*-
import arcpy, os
import glob
from arcpy.sa import *
arcpy.CheckOutExtension("Spatial")

# .nc files path
# 工作空间
nc_folder = r'F:\data\xyz-O3\S5P\workspace\workspace-2022-20220501'
# tif文件夹
tif_folder = os.path.join(nc_folder, '2tif')
# grid count 计算后文件夹
grid_folder = os.path.join(nc_folder, '3count')
# 镶嵌 后 文件夹
mosaic_folder_mean = os.path.join(nc_folder, 'masaic_folder_mean')
# 镶嵌 后 文件夹
mosaic_folder_min = os.path.join(nc_folder, '4hebing')
#  裁剪文件夹
clip_folder = os.path.join(nc_folder, '5clip')
# .shp file path
mask_shp = r"D:\work\python\data\china\国界.shp"

def grid_count():
	#  去黑边  之后才能进行镶嵌

	# 读取文件
	if not os.path.exists(grid_folder):
		os.makedirs(grid_folder)

	search_criteria = "*.tif"
	q = os.path.join(tif_folder, search_criteria)
	tif_list = glob.glob(q)

	for i in tif_list:
		r = Raster(i)  # 打开栅格
		newRaster = r * 1
		path, filename = os.path.split(i)
		output = grid_folder + os.path.sep + filename
		newRaster.save(output)  # 保存


def mosaicRaster_mean(tif_list):
	if not os.path.exists(mosaic_folder_mean):
		os.makedirs(mosaic_folder_mean)
	arcpy.env.workspace = grid_folder
	num_2 = 0
	num_list, mosaic_list = [], []
	# Identify the same day's raster, the different dateset has different identity. In the VIIRS product, we decided the raster is [:28]
	for raster in tif_list:
		num = raster[:18]
		if num not in num_list:
			num_list.append(num)
	# Mosaic the same day's raster
	for num in num_list:
		mosaic_list_2 = []
		for raster in tif_list:
			if raster[:28] == num:
				mosaic_list_2.append(raster)
				name = raster[:28] + '.tif'
		# Mosaic to new raster. Noticed the datatype: 32_BIT_FLOAT
		arcpy.env.snapRaster = name
		arcpy.MosaicToNewRaster_management(mosaic_list_2, mosaic_folder_mean, name, "", "64_BIT", 0.1, "1", "MEAN", "FIRST")
		mosaic_list.append(name)
		num_2 += 1
		print('Mosaic: ' + name)
	print('Numbers: ', num_2)
	print('-'*50)
	return mosaic_list,mosaic_folder_mean

def mosaicRaster_min(tif_list):
	if not os.path.exists(mosaic_folder_min):
		os.makedirs(mosaic_folder_min)
	arcpy.env.workspace = grid_folder
	num_2 = 0
	num_list, mosaic_list = [], []
	# Identify the same day's raster, the different dateset has different identity. In the VIIRS product, we decided the raster is [:28]
	for raster in tif_list:
		num = raster[:13]
		if num not in num_list:
			num_list.append(num)
	# Mosaic the same day's raster
	for num in num_list:
		mosaic_list_2 = []
		for raster in tif_list:
			if raster[:13] == num:
				mosaic_list_2.append(raster)
				name = raster[:13] + '.tif'
		# Mosaic to new raster. Noticed the datatype: 32_BIT_FLOAT
		arcpy.env.snapRaster = name
		arcpy.MosaicToNewRaster_management(mosaic_list_2, mosaic_folder_min, name, "", "64_BIT", 0.05, "1", "MINIMUM", "FIRST")
		mosaic_list.append(name)
		num_2 += 1
		print('Mosaic: ' + name)
	print('Numbers: ', num_2)
	print('-'*50)
	return mosaic_list,mosaic_folder_min

def clipRaster(mosaic_list,mosaic_folder):
	if not os.path.exists(clip_folder):
		os.makedirs(clip_folder)
	arcpy.env.workspace = mosaic_folder
	num = 0
	for in_raster in mosaic_list:
		# Execute ExtractByMask
		arcpy.env.snapRaster = in_raster
		clip_name = in_raster[:-4] + '_China' + '.tif'
		prj_clip = clip_folder + '\\' + clip_name
		outClip = ExtractByMask(in_raster, mask_shp)
		outClip.save(prj_clip)
		num += 1
		print(clip_name)
	print('Numbers: ', num)
	print('-'*50)

# def main():
# 	if not os.path.exists(mosaic_folder):
# 		os.makedirs(mosaic_folder)
# 	tif_list = os.listdir(tif_folder)
# 	mosaic_list = mosaicRaster(tif_list)
# 	clipRaster(mosaic_list)


def main1(type):
	# grid_count()
	# 读取文件
	search_criteria = "*.tif"
	q = os.path.join(grid_folder, search_criteria)
	list = glob.glob(q)
	tif_list = []
	for i in list:
		path, filename = os.path.split(i)
		tif_list.append(filename)
	mosaic_list,mosaic_folder = mosaicRaster_min(tif_list)
	# clipRaster(mosaic_list,mosaic_folder)

if __name__ == "__main__":
	type = {
		"min_mosaic" : 1,
		"mean_mosaic" : 2,
	}


	main1(type["min_mosaic"])