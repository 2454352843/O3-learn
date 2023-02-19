import glob
import os
import shutil


def main():
    inputpath = r'E:\data\6. site\5yuedataset\1totif'
    outputpath = r'E:\data\6. site\5yuedataset\2finally'


    tiffiles = glob.glob(inputpath + os.path.sep + '*.tif')
    for tiff in tiffiles:
        name = tiff.split(os.path.sep)[-1]
        print(name)
        day = name[:10]
        outdir = outputpath + os.path.sep + day

        if not os.path.exists(outdir):
            os.makedirs(outdir)

        output = outdir + os.path.sep +'site_' + name
        shutil.copy(tiff,output)



if __name__ == '__main__':
    main()