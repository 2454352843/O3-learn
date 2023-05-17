# -*- coding: utf-8 -*-

import sys
import os
import glob
import numpy as np
import csv
from osgeo import gdal, ogr, osr
from osgeo import gdalconst
from pykrige.ok import OrdinaryKriging
# from tqdm import trange
from scipy.spatial import cKDTree
import math

'''
各类插值算法

'''

def nearDeal(infile,outfile,xsize,ysize):

    """最邻近重采样"""

    ds = gdal.Open(infile)
    options = gdal.TranslateOptions(format='GTiff', width=xsize, height=ysize, resampleAlg=gdalconst.GRA_NearestNeighbour)
    ds = gdal.Translate(outfile, ds, options=options)
    
    del ds 

def bilinearDeal(infile,outfile,xsize,ysize):

    """重采样"""
    # GRA_Mode

    ds = gdal.Open(infile)
    options = gdal.TranslateOptions(format='GTiff', width=xsize, height=ysize, resampleAlg=gdalconst.GRA_Bilinear)
    ds = gdal.Translate(outfile, ds, options=options)
    
    del ds 

def cubicDeal(infile,outfile,xsize,ysize) -> object:

    """重采样"""
    # GRA_Mode

    ds = gdal.Open(infile)
    options = gdal.TranslateOptions(format='GTiff', width=xsize, height=ysize, resampleAlg=gdalconst.GRA_Cubic)
    ds = gdal.Translate(outfile, ds, options=options)
    
    del ds 

def cubicsplineDeal(infile,outfile,xsize,ysize):

    """重采样"""
    # GRA_Mode

    ds = gdal.Open(infile)
    options = gdal.TranslateOptions(format='GTiff', width=xsize, height=ysize, resampleAlg=gdalconst.GRA_CubicSpline)
    ds = gdal.Translate(outfile, ds, options=options)
    
    del ds 

def lanczosDeal(infile,outfile,xsize,ysize):

    """重采样"""
    # GRA_Mode

    ds = gdal.Open(infile)
    options = gdal.TranslateOptions(format='GTiff', width=xsize, height=ysize, resampleAlg=gdalconst.GRA_Lanczos)
    ds = gdal.Translate(outfile, ds, options=options)
    
    del ds 

def averageDeal(infile,outfile,xsize,ysize):

    """重采样"""
    # GRA_Mode

    ds = gdal.Open(infile)
    options = gdal.TranslateOptions(format='GTiff', width=xsize, height=ysize, resampleAlg=gdalconst.GRA_Average)
    ds = gdal.Translate(outfile, ds, options=options)
    
    del ds 

def modeDeal(infile,outfile,xsize,ysize):

    """重采样"""
    # GRA_Mode

    ds = gdal.Open(infile)
    options = gdal.TranslateOptions(format='GTiff', width=xsize, height=ysize, resampleAlg=gdalconst.GRA_Mode)
    ds = gdal.Translate(outfile, ds, options=options)
    
    del ds 

def KringDeal(minLon,maxLon,minLat,maxLat,lines,columns,Lonarr, Latarr, Valuearr):

    # 克里金插值

    # grid_lon = np.linspace(111.35,115.43,408)
    # grid_lat = np.linspace(21.56,24.40,284)

    grid_lon = np.linspace(minLon,maxLon,columns)
    grid_lat = np.linspace(minLat,maxLat,lines)

    print("start")
    OK = OrdinaryKriging(Lonarr, Latarr, Valuearr, variogram_model='spherical',nlags=6)#球形插值
    print("end")
    z1, ss1 = OK.execute('grid', grid_lon, grid_lat)
    print("ok")

    return z1

