import os, shutil
import glob

import pandas as pd
from pandas import ExcelWriter
from tqdm import tqdm

'''
1.转换，csv转xlsx。
2.合并csv，转换为第一批数据格式
'''

input_1 = r''
input_2 = r'I:\data\xyz-O3\site\第二批\China_O3'
output_path = r'I:\data\xyz-O3\site\workspace'


def main():
    # 1.循环读取第二批数据
    for root, dirs, files in os.walk(input_2):
        if (len(files) <= 0):
            continue
        file_list = []
        for file in files:
            if not file.endswith('.csv'):
                continue
            file_list.append(root + os.path.sep + file)

        # 2.根据日期读取数据
        df_list = []
        len_num = 0
        for i in (range(len(file_list))):
            csvfile = file_list[i]
            # print(xlsxfile.split(os.path.sep)[-1])
            date = csvfile.split(os.path.sep)[-1][:-5].replace('-', '_')
            df = pd.read_csv(csvfile)
            # df = pd.read_excel(csvfile)
            # df1 = df[df['Time'] == f'00:00:00.0000000']
            # for i in df["Time"]:
            #     str1 = f'0{str(i)}:00:00.0000000' if i <10 else f'{str(i)}:00:00.0000000'
            #     print(str1)
            df["Time"] = [f'0{str(i)}:00:00.0000000' if i < 10 else f'{str(i)}:00:00.0000000' for i in df["Time"]]

            len_num += len(df)
            df_list.append(df)

        # 3. 合并df，并保存为xlsx
        df_out = df_list[0]
        for i in range(len(df_list) - 1):
            df = df_list[i + 1]
            df_out  = pd.concat([df_out,df])

        print(f"数据共有{len_num}条,df长度为{len(df_out)}")
        output_file = output_path + os.path.sep + f"{os.path.split(root)[1]}.xlsx"
        with ExcelWriter(output_file) as writer:
            df_out.to_excel(writer)

if __name__ == '__main__':
    main()
