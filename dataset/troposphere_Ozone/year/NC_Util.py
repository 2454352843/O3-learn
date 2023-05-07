# -*- coding: utf-8 -*-

import sys
import os
import netCDF4 as nc
import numpy as np

"""
    NC数据文件读写操作 
     
"""

# 打开nc文件
def NCopen(ncfile):

    # load in the netCDF4 file  
    ncdata = nc.Dataset(ncfile) 

    return ncdata

    # read the variables from the netCDF4 file and assign 


#获取数据数组1
def ReadNcDataset1(ncdata,datasetPath):

    if datasetPath in ncdata.variables.keys():

        dataset = ncdata.variables[datasetPath]

        dataset1 = np.array(dataset)

    return dataset1

#获取数据数组2
def ReadNcDataset2(ncdata,datasetPath):

    if datasetPath in ncdata.variables.keys():

        dataset = ncdata.variables[datasetPath][:,:]

        dataset1 = np.array(dataset)

    return dataset1


#获取数据数组3
def ReadNcDataset3(ncdata,datasetPath):

    if datasetPath in ((ncdata.groups)["PRODUCT"]).variables.keys():

        dataset = ((ncdata.groups)["PRODUCT"]).variables[datasetPath]

        dataset1 = np.array(dataset)

    return dataset1



# 关闭nc文件
def NCclose(ncdata):

    ncdata.close()


