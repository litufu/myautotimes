import pandas as pd
import os
from settings.utils import std_input_data,get_std_stock



def handle_single_df(df):

    df_copy = get_std_stock(df)
    df_copy = std_input_data(df_copy)

    return df_copy


# 获取D:\BaiduNetdiskDownload\stock\minute15中所有的文件夹
def get_all_stocks(folder_path):

    folders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]
    # ['2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024']
    # 取出所有文件夹中的csv文件名并去除重复项，将文件名中的“.csv”替换为“”
    file_names = set()
    for folder in folders:
        folder_path = os.path.join(r'D:\BaiduNetdiskDownload\stock\minute15', folder)
        for file in os.listdir(folder_path):
            if file.endswith('.csv'):
                file_name = file.replace('.csv', '')
                file_names.add(file_name)
    # 将file_names转换为列表并排序
    file_names = sorted(list(file_names))
    print(file_names)
    return file_names

# 给定一个股票代码，获取该股票在D:\BaiduNetdiskDownload\stock\minute15中所有年份的csv文件，并将这些csv文件中的数据合并成一个DataFrame，返回该DataFrame
def get_stock_data(root_path,stock_code):
    folders = [f for f in os.listdir(root_path) if os.path.isdir(os.path.join(r'D:\BaiduNetdiskDownload\stock\minute15', f))]
    df_list = []
    for folder in folders:
        file_path = os.path.join(root_path, folder, stock_code + '.csv')
        if os.path.exists(file_path):
            # df = handle_single_csv(file_path)
            df = pd.read_csv(file_path)
            df_list.append(df)
    if len(df_list) > 0:
        df_all = pd.concat(df_list, ignore_index=True)
        df_all = handle_single_df(df_all)
        return df_all
    else:
        print(f'没有找到股票代码为{stock_code}的csv文件')
        return None




if __name__ == '__main__':
    folder = r'D:\BaiduNetdiskDownload\stock\minute15'
    get_all_stocks(folder)
    # stock_code = 'SH.600036'
    # root_path = r'D:\BaiduNetdiskDownload\stock\minute15'
    # df_stock = get_stock_data(root_path,stock_code)
    # print(df_stock)
    # df_stock.to_csv(r'SH.600036_all.csv', index=False)

