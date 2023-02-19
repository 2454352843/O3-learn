import os
import shutil

import config.log
from dataset.total_column_ozone.Surface_Ozone_NC_to_TIF import surface_S5Preprocess

os.environ['NUMEXPR_MAX_THREADS']='16'
from dataset.total_column_ozone import fusion
from dataset.total_column_ozone.Ozone_NC_to_TIF import S5Preprocess
from utils.read_tif import readtif
import glob

logger = config.log.getLogger()

def s5p_tropomi_ozone_toTif(input_floder,output_floder):
    # 1 nc转tif

    hdf_folder = input_floder
    hdf_files = os.listdir(hdf_folder)
    file_paths = []
    for file in hdf_files:
        file_paths.append(hdf_folder + "\\" + file)
    outpath = output_floder
    print(f"file_paths:{file_paths}")
    value = 75  # 质量控制值, int
    result = S5Preprocess().main(file_paths, outpath, value)
    # result = S5Preprocess().main(file_paths,outpath,value,spatial_res=[835,77])

def surface_s5p_tropomi_ozone_toTif(input_floder,output_floder):
    # 1 nc转tif

    search_criteria = "*.nc"
    q = os.path.join(input_floder, search_criteria)
    print(q)

    # 获取输入路径
    #  O3_20200101T005246_ozone_total_vertical_column.tif
    input_files = glob.glob(q)

    outpath = output_floder

    value = 75  # 质量控制值, int
    result = surface_S5Preprocess().main(input_files, outpath, value)
    # result = S5Preprocess().main(file_paths,outpath,value,spatial_res=[835,77])


def s5p_cut(workspace):
    # 2 输出裁剪

    input = workspace + os.sep + 'Ozone'
    output = workspace + os.sep + 'cut'
    if not os.path.exists(output):
        os.mkdir(output)
    readtif().tifCut(input, output)


def tif_fusion(workspace):


    input = workspace + os.sep + 'cut'
    output = workspace + os.sep + 'fusion'
    if not os.path.exists(output):
        os.mkdir(output)


    # 3 图片融合
    fusion.main(input_floder=input,
                output_floder=output)


def conversion(workspace):

    input = workspace + os.sep + 'fusion'
    output = workspace + os.sep + 'out'
    if not os.path.exists(output):
        os.mkdir(output)


    readtif().conversion(input,output)

def clear(workspace):
    # 删除多于文件
    search_criteria = "*.nc"
    q = os.path.join(workspace, search_criteria)

    # 获取输入路径
    #  O3_20200101T005246_ozone_total_vertical_column.tif
    input_files = glob.glob(q)
    for i in input_files:

        if( i[-4:-3] == ')'):
            if os.path.isfile(i):
                try:
                    logger.info("delete {i}".format(i=i))
                    os.remove(i)  # 这个可以删除单个文件，不能删除文件夹
                except BaseException as e:
                    print(e)

    # 删除非nc后缀文件和文件夹
    search_criteria = "*.nc"
    q = os.path.join(workspace, search_criteria)
    input = glob.glob(q)
    allFile = os.listdir(workspace)
    inputfile = []
    for i in input:
        inputfile.append(os.path.basename(i))

    notfile = list(set(allFile)^set(inputfile))
    print(notfile)

    for i in notfile:
        i = os.path.join(workspace,i)
        if os.path.isfile(i) :
            try:
                logger.info("delete {i}".format(i=i))
                os.remove(i)  # 这个可以删除单个文件，不能删除文件夹
            except BaseException as e:
                print(e)
        if os.path.isdir(i) :
            try:
                logger.info("delete {i}".format(i=i))
                shutil.rmtree(i)  # 删除文件夹
            except BaseException as e:
                print(e)



if __name__ == '__main__':

    # clear(r'D:\work\python\data\tif\O3\troposphere\test')

    #输入输出
    input_floder = r'D:\work\python\data\nc\troposphere\202107-202205'
    output_floder = r'D:\work\python\data\tif\O3\troposphere\202107-202205'

    # clear(input_floder)
    #
    #
    # # s5p_tropomi_ozone_toTif(input_floder,output_floder)
    # surface_s5p_tropomi_ozone_toTif(input_floder,output_floder)
    #
    #
    # s5p_cut(output_floder)

    tif_fusion(output_floder)

    conversion(output_floder)

    logger.info("结束")
