# -*- coding: utf-8 -*-
import arcpy, os
import glob
from arcpy.sa import *
arcpy.CheckOutExtension("Spatial")

# .nc files path
# 工作空间
nc_folder = r'E:\data\3. SILAM\workspace'
# tif文件夹
reshape_folder = os.path.join(nc_folder, '3reshape')

#  裁剪文件夹
clip_folder = os.path.join(nc_folder, '4clip')
# .shp file path
mask_shp = r"D:\work\python\data\china\国界.shp"



def clipRaster(reshape_folder):
	if not os.path.exists(clip_folder):
		os.makedirs(clip_folder)
	arcpy.env.workspace = reshape_folder

	mosaic_list = glob.glob(reshape_folder +os.path.sep+ "*.tif")
	num = 0
	for in_raster in mosaic_list:
		# Execute ExtractByMask
		arcpy.env.snapRaster = in_raster
		clip_name = in_raster[:-13].split(os.path.sep)[-1] + '_China' + '.tif'
		prj_clip = clip_folder + '\\' + clip_name
		outClip = ExtractByMask(in_raster, mask_shp)
		outClip.save(prj_clip)
		num += 1
		print(clip_name)
	print('Numbers: ', num)
	print('-'*50)

def main():


	clipRaster(reshape_folder)




if __name__ == "__main__":
	main()