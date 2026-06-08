import pandas as pd
import os
from settings.utils import get_std_trade_date



def handle_single_df(df):
    
    # 将df中的“日期”和“时间”两列合并成一个新的“datetime”列，并将其转换为datetime类型
    df['date'] = pd.to_datetime(df['日期'] + ' ' + df['时间'])
    # 将“日期”和“时间”两列删除
    df.drop(['日期', '时间'], axis=1, inplace=True)
    # 将“代码”和“复权状态”两列删除
    df.drop(['代码', '复权状态'], axis=1, inplace=True)
    # 将“开盘”列重命名为“open”，“收盘”列重命名为“close”，“最高”列重命名为“high”，“最低”列重命名为“low”，“成交量(股)”列重命名为“volume”,“成交金额(元)”列重命名为“amount”
    df.rename(columns={'开盘': 'open', '收盘': 'close', '最高': 'high', '最低': 'low', '成交量(股)': 'volume', '成交金额(元)': 'amount'}, inplace=True)
    # 复制一份df，并将复制的df命名为df_copy，保留df_copy中的“datetime”、“open”、“close”、“high”、“low”,“volume”,“amount”列
    df_copy = df[['date', 'open', 'close', 'high', 'low', 'volume', 'amount']].copy()
    # 获取标准的交易日期列表
    std_trade_date = get_std_trade_date()
    # 按照df_copy中的“date"列的第一个值作为起始日期，最后一个值作为结束日期，获取这段时间内的标准交易日期列表
    std_trade_date = std_trade_date[(std_trade_date['date'] >= df_copy['date'].iloc[0]) & (std_trade_date['date'] <= df_copy['date'].iloc[-1])]
    # 将df_copy中的“date”列与std_trade_date中的date标准进行对比，
    df_copy = df_copy.set_index('date')
    df_copy = df_copy.reindex(std_trade_date['date'])
    # 对于df_copy缺失的行，按照其前一个交易日的close作为open、close、high、low的值，并将volume和amount设置为0，补齐df_copy中的缺失行
    df_copy['close'] = df_copy['close'].ffill()
    # 将df_copy中的缺失行的open、high、low的值设置为close的值
    df_copy['open'] = df_copy['open'].fillna(df_copy['close'])
    df_copy['high'] = df_copy['high'].fillna(df_copy['close'])
    df_copy['low'] = df_copy['low'].fillna(df_copy['close'])
    df_copy['volume'] = df_copy['volume'].fillna(0)
    df_copy['amount'] = df_copy['amount'].fillna(0)

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
    # folder = r'D:\BaiduNetdiskDownload\stock\minute15'
    # get_all_stocks(folder)
    stock_code = 'SH.600036'
    root_path = r'D:\BaiduNetdiskDownload\stock\minute15'
    df_stock = get_stock_data(root_path,stock_code)
    print(df_stock)
    # df_stock.to_csv(r'SH.600036_all.csv', index=False)

