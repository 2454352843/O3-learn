# 数据介绍
s5p卫星数据 tropomi传感器

`下载网址` https://disc.gsfc.nasa.gov/datasets?keywords=O3%20tropomi&page=1

`下载方式`  火狐插件  IDM下载

`单位` 
# 数据处理

`单位` mol m-2

`标准单位` DU  DU/mol =   2241.149902

`分辨率` 0.3 度

## 处理流程
1.surface_nc_to_tif.py

tif转nc，使用库为nc4

2.tif_mosaic_clip.py

图像去黑边，图像融合，拼接。使用python2.7，使用arcpy。

3.单位转换

使用代码和总柱浓度代码一样，单位为mol 转 DU

4. 缺失补全  missingCompleting.py

5. resample_1processed

重采样，分辨率调整为0.01