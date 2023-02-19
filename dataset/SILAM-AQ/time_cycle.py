import glob
import os
import shutil

inputpath = r"E:\data\3. SILAM\workspace\4clip" + os.path.sep
outputpath = r"E:\data\3. SILAM\workspace\5time" + os.path.sep


def time_cycle(filepath):
    filename = filepath.split(os.path.sep)[-1]
    tmp = filename[-18:-10]
    tmp_hour = int(tmp[-1:])
    hour = int(tmp[-5:-2])
    hour = hour + tmp_hour - 1 + 8

    if (hour < 10):
        hour = '0' + str(hour)
    else:
        hour = str(hour)

    lastname = filename[:-18] + hour + '.tif'


    shutil.copy(filepath,outputpath+lastname)

    # print(filename[-18:-10])


def main():
    tiffiles = glob.glob(inputpath + "*.tif")

    for file in tiffiles:
        time_cycle(file)


if __name__ == '__main__':
    main()
