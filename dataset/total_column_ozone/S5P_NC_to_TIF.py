
import os
import random
import string
from osgeo import gdal
import numpy as np

class S5Preprocess:
	'''
	将S5P原始数据转换为tif格式，默认坐标系为84坐标系
	'''
	def __init__(self):
		# 默认处理波段，也可以自行更改或添加
		self.field =  {'SO2':['sulfurdioxide_total_vertical_column']}

	def write_s5p_tif(self, in_filepath, variables, output_folder, EPSG_code="4326", spatial_res=[]):
		"""
		将特定变量的S5P nc文件转换为带坐标系的tif文件
		S5P默认栅格大小为3500*7000

		in_filepath: str nc文件全路径
		variables: list of str 所需转换的变量名称
		EPSG_code: str 坐标系
		spatial_res: list of float, x 和 y 像元大小 默认为3500*7000
		"""
		flag = False
		kwargs = {}
		kwargs['EPSG_code'] = EPSG_code
		kwargs['spatial_res'] = spatial_res
		# Create vrt files for latitude and longitude variables
		geo_params = {}
		geo_params['outputSRS'] = "EPSG:{EPSG_code}".format(EPSG_code=EPSG_code)
		gdal.Translate("lat.vrt", 'HDF5:"{in_filepath}"://PRODUCT/latitude'.format(in_filepath=in_filepath), **geo_params)
		lat_ds = gdal.Open("lat.vrt")
		gdal.Translate("lon.vrt", 'HDF5:"{in_filepath}"://PRODUCT/longitude'.format(in_filepath=in_filepath), **geo_params)
		random_data = ''.join(random.sample(string.ascii_letters + string.digits, 6)) + '.tif'
		random_mask = ''.join(random.sample(string.ascii_letters + string.digits, 6)) + '.tif'
		data_var = random_data
		mask_var = random_mask

		for variable in variables:
			output_file = self.generate_out_filepath(in_filepath, output_folder, variable, ".tif")

			# Georeference variable datset
			self.write_var_to_tif(data_var, in_filepath, variable, "lon.vrt", "lat.vrt", lat_ds, **kwargs)
			# Georeference quality_value datset
			self.write_var_to_tif(mask_var, in_filepath, "qa_value", "lon.vrt", "lat.vrt", lat_ds, **kwargs)
			# Apply quality mask to variable dataset
			if os.path.isfile(data_var) and os.path.isfile(mask_var):
				self.write_masked_data(output_file, data_var, mask_var, self.threshold)
				flag = True
				# Clean
				os.remove(data_var)
				os.remove(data_var.split('.')[0] + '_.vrt')
				os.remove(mask_var)
				os.remove(mask_var.split('.')[0] + '_.vrt')
			else:
				flag = False
				# Clean
				os.remove(data_var.split('.')[0] + '_.vrt')
				os.remove(mask_var.split('.')[0] + '_.vrt')
		# Remove vrt files
		del lat_ds
		os.remove('lon.vrt')
		os.remove('lat.vrt')
		return flag


	def write_var_to_tif(self,out_filepath, in_filepath, variable, lon_file, lat_file, ds, **kwargs):
		'''
		动态撰写vrt虚拟栅格文件
		:param out_filepath: 输出文件路径
		:param in_filepath: 输入文件路径
		:param variable: 变量名称
		:param lon_file: 经度vrt文件
		:param lat_file: 纬度vrt文件
		:param ds: 包含输出信息的dataset
		:param kwargs:不定长参数 包含坐标信息 分辨率等
		:return: None
		'''
		vrt_filepath = out_filepath.split('.')[0] + '_.vrt'
		meta = '''
		<VRTDataset rasterXSize="{RasterXSize}" rasterYSize="{RasterYSize}">
			<metadata domain="GEOLOCATION">
				<mdi key="X_DATASET">{lon_file}</mdi>
				<mdi key="X_BAND">1</mdi>
				<mdi key="Y_DATASET">{lat_file}</mdi>
				<mdi key="Y_BAND">1</mdi>
				<mdi key="PIXEL_OFFSET">0</mdi>
				<mdi key="LINE_OFFSET">0</mdi>
				<mdi key="PIXEL_STEP">1</mdi>
				<mdi key="LINE_STEP">1</mdi>
			</metadata> 
			<VRTRasterBand band="1" datatype="Float32">
				<SimpleSource>
					<SourceFilename relativeToVRT="0">HDF5:{in_filepath}://PRODUCT/{variable}</SourceFilename>
					<SourceBand>1</SourceBand>
					<SourceProperties RasterXSize="{RasterXSize}" RasterYSize="{RasterYSize}" DataType="Float32" BlockXSize="{RasterXSize}" BlockYSize="{RasterYSize}" />
					<SrcRect xOff="0" yOff="0" xSize="{RasterXSize}" ySize="{RasterYSize}" />
					<DstRect xOff="0" yOff="0" xSize="{RasterXSize}" ySize="{RasterYSize}" />
				</SimpleSource>
			</VRTRasterBand>
		</VRTDataset>
		'''.format(RasterXSize = ds.RasterXSize,RasterYSize = ds.RasterYSize,in_filepath = in_filepath,lon_file = lon_file,lat_file = lat_file,variable = variable)
		print(meta)
		with open(vrt_filepath, "w") as text_file:
			text_file.write(meta)
		# Add georeferencing to vrt file
		self.georef_data(out_filepath, vrt_filepath, vrt=False, **kwargs)

	def write_masked_data(self,out_filepath, data_file, mask_file, mask_threshold):
		'''
		掩膜文件输出
		:param out_filepath: 输出文件全路径
		:param data_file: 输入处理数据
		:param mask_file: 输入掩膜数据
		:param mask_threshold: 掩膜阈值
		:return: None
		'''
		data_ds = gdal.Open(data_file)
		data = data_ds.ReadAsArray()
		mask = gdal.Open(mask_file).ReadAsArray()
		data[mask <= mask_threshold] = np.nan
		driver = gdal.GetDriverByName('GTiff')
		dataset = driver.Create(
			out_filepath,
			data_ds.RasterXSize,
			data_ds.RasterYSize,
			1,
			gdal.GDT_Float32, )
		dataset.SetGeoTransform(data_ds.GetGeoTransform())
		dataset.SetProjection(data_ds.GetProjectionRef())
		dataset.GetRasterBand(1).WriteArray(data)
		dataset.FlushCache()  # Write to disk.

	def georef_data(self,out_filepath, in_filepath, vrt, EPSG_code, spatial_res):
		'''
		文件写出
		:param out_filepath: 输出文件路径
		:param in_filepath: 输入文件
		:param vrt: True: 输入文件不是vrt,False: 输入文件为vrt
		:param EPSG_code:坐标系编码
		:param spatial_res:分辨率
		:return:None
		'''

		params = {}
		params['dstNodata'] = -9999
		params['dstSRS'] = "EPSG:{EPSG_code}".format(EPSG_code=EPSG_code)
		if vrt:
			params["format"] = "VRT"
			out_filepath = out_filepath.replace('.tif', '.vrt')
		else:
			params["format"] = "Gtiff"
			out_filepath = out_filepath.replace('.vrt', '.tif')
		if not spatial_res:
			if EPSG_code == "4326":
				params['xRes'] = 0.06288  # equivalent to 7000 meters
				params['yRes'] = 0.06288  # equivalent to 7000 meters
			else:
				params['xRes'] = 7000  # meters
				params['xRes'] = 7000  # meters
		else:
			params['xRes'] = spatial_res[0]
			params['xRes'] = spatial_res[1]

		try:
			gdal.Warp(out_filepath, in_filepath, **params)
		except Exception as e:
			print(e)

	def generate_out_filepath(self,in_filepath, output_folder, v_name,ext='.tif'):
		'''
		输出文件命名
		:param in_filepath:输入文件名称全路径 str
		:param output_folder:输出文件夹 str
		:param v_name:变量名称 str
		:param ext:输出格式
		:return:输出文件名
		'''
		f_path, f_name = os.path.split(in_filepath)
		filename, txt = os.path.splitext(f_name)
		var_name_short = filename[13:20].replace('_','')
		timestamp = filename[20:35]
		return output_folder + os.path.sep + var_name_short + '_' + timestamp + '_' + v_name + ext

	def get_product_name(self,in_filepath):
		f_path,f_name = os.path.split(in_filepath)
		basename,txt = os.path.splitext(f_name)
		var_name_short = basename[13:20].replace('_', '')
		return var_name_short

	def main(self,files,outpath,value=75):
		self.threshold = value
		crashed_file = {'crashed_image':[]}
		x = []
		msg_outpath = []
		for f in files:
			name = S5Preprocess().get_product_name(f)
			var = self.field[name]
			print(var)
			outpath_ = outpath + os.sep + name
			if not os.path.exists(outpath_):
				os.mkdir(outpath_)
			msg_outpath.append(outpath_)
			flag = self.write_s5p_tif(f, var, outpath_) # f:文件 var: 需要字段  outpath_：输出文件夹
			if not flag:
				x.append(f)
		crashed_file['crashed_image'] = x
		if x ==[]:
			msg = None
		else:
			msg = crashed_file
		msg_out = {'outpath': msg_outpath}
		return msg,msg_out

if __name__ == '__main__':
	# hdf_folder = r'C:\Users\admin\Desktop\so2'
	hdf_folder = r'D:\work\python\pycharm\Sentinel\resource\so2'
	hdf_files = os.listdir(hdf_folder)
	file_paths = []
	for file in hdf_files:
		file_paths.append(hdf_folder + "\\" + file)
	outpath = r'D:\work\python\pycharm\Sentinel\resource\output\so2'
	print(f"file_paths:{file_paths}")
	value = 75 # 质量控制值, int
	result = S5Preprocess().main(file_paths,outpath,value)
	print(result)
