
img_list = ['PS','T2M','TROPCOL_O3','U2M','V2M','ZPBL','SILAM','Tropomi','DEM','NDVI','POP','pri_sec']
path = r'D:\work\python\pycharm\O3-learn\Pytorch\O3_estimate\Resource\math1.txt'

# 返回数据集中使用的mean,std
def get_math():


    mean_list = []
    std_list = []
    max_list = []
    min_list = []

    with open(path, 'r', encoding='utf-8') as f:
        imgs_info = f.readlines()
        imgs_info = list(map(lambda x: x.strip().split('\t'), imgs_info))

    txt = imgs_info

    for i in img_list:
        for j in txt:
            if (i in j[0]):
                # print(i,j[0])
                mean_list.append(j[3])
                std_list.append(j[4])
                max_list.append(j[1])
                min_list.append(j[2])

    # for i in range(12):
    #     print(img_list[i], mean_list[i], std_list[i])

    return mean_list,std_list,max_list,min_list


# 进行归一化
def normalization(data,max_data,min_data):
    min_data = float(min_data)
    _range = float(max_data) - min_data
    return (data - min_data) / _range

if __name__ == '__main__':
    get_math()