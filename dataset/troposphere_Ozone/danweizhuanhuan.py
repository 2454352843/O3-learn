import logging
import arcpy, os
import glob
from arcpy.sa import *
arcpy.CheckOutExtension("Spatial")
logger = logging.getLogger()


def arcpy_conversion():

	input = r'E:\data\1. S5P_OFFL_L2_O3\workspace\5clip'
	output = r'E:\data\1. S5P_OFFL_L2_O3\workspace\6finally\6finally'  # type: str

	if not os.path.exists(output):
		os.makedirs(output)

	search_criteria = "*.tif"
	q = os.path.join(input, search_criteria)
	tif_list = glob.glob(q)

	for i in tif_list:
		r = Raster(i)
		newRaster = r * 2241.149902
		path, filename = os.path.split(i)
		output1 = output + os.path.sep + filename
		newRaster.save(output1)
		logger.info("{output1} end".format(output1=output1))

arcpy_conversion()