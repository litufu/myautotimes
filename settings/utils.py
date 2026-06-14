import pathlib
import pandas as pd
import os
import torch
from setting import dataset_path

# 获取当前文件 (utils.py) 的绝对路径
# __file__ 是当前脚本的路径
# .resolve() 解析符号链接，确保路径真实
# .parent 获取所在目录
BASE_DIR = pathlib.Path(__file__).resolve().parent

# 获取查询日期对应的前ndays个对应的交易日期
def get_trade_date(query_date,ndays):
    # 拼接出数据文件的绝对路径
    file_path = BASE_DIR / "trade_cal.csv"
    # 读取csv文件并返回DataFrame
    df = pd.read_csv(file_path)
    # 将日期列转换为datetime类型
    df['cal_date'] = pd.to_datetime(df['cal_date'], format='%Y%m%d')
    # 获取查询日期对应的行
    query_date = pd.to_datetime(query_date)
    # 获取start对应的交易日期
    start_date = query_date.strftime("%Y-%m-%d")
    # 获取start对应的交易时间
    start_time = query_date.strftime("%H:%M:%S")

    query_row = df[df['cal_date'] == start_date]
    if query_row.empty:
        raise Exception(f'查询日期{query_date}不在交易日历中')
    # 获取查询日期对应的索引
    query_index = query_row.index[0]
    count = 0
    # 逐个向前遍历，直到找到ndays个交易日期
    while count < ndays and query_index > 0:
        query_index -= 1
        if df['is_open'].iloc[query_index] == 1:
            count += 1

    trade_date = df["cal_date"].iloc[query_index]
    result = trade_date.strftime("%Y-%m-%d") + ' ' + start_time
    return result

def get_std_trade_date():
    # 拼接出数据文件的绝对路径
    file_path = BASE_DIR / "stock.csv"
    df = pd.read_csv(file_path, parse_dates=['date'])
    # 按照date列升序排序
    df = df.sort_values(by='date').reset_index(drop=True)
    return df


def std_input_data(df_copy):
    # 获取标准的交易日期列表
    std_trade_date = get_std_trade_date()
    # 按照df_copy中的“date"列的第一个值作为起始日期，最后一个值作为结束日期，获取这段时间内的标准交易日期列表
    std_trade_date = std_trade_date[
        (std_trade_date['date'] >= df_copy['date'].iloc[0]) & (std_trade_date['date'] <= df_copy['date'].iloc[-1])]
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
    # 将df_copy中的索引重置为默认的整数索引，并将date列移动到第一列
    df_copy = df_copy.reset_index()
    return df_copy


def get_stamp(df_raw):
    std_trade_date = get_std_trade_date()
    start_date = df_raw['date'].iloc[0]
    end_date = df_raw['date'].iloc[-1]
    start_index = std_trade_date[std_trade_date['date'] == start_date].index[0]
    end_index = std_trade_date[std_trade_date['date'] == end_date].index[0]
    data_stamp = torch.load(os.path.join(dataset_path, 'stock.pt'))
    # 从data_stamp中取出起始索引到结束索引的数据作为data_stamp
    data_stamp = data_stamp[start_index:end_index + 1]
    # 重置self.data_stamp的索引，使其从0开始
    data_stamp.index = range(len(data_stamp))
    return data_stamp

def get_std_stock(df):
    # 将df中的“日期”和“时间”两列合并成一个新的“datetime”列，并将其转换为datetime类型
    df['date'] = pd.to_datetime(df['日期'] + ' ' + df['时间'])
    # 将“日期”和“时间”两列删除
    df.drop(['日期', '时间'], axis=1, inplace=True)
    # 将“代码”和“复权状态”两列删除
    df.drop(['代码', '复权状态'], axis=1, inplace=True)
    # 将“开盘”列重命名为“open”，“收盘”列重命名为“close”，“最高”列重命名为“high”，“最低”列重命名为“low”，“成交量(股)”列重命名为“volume”,“成交金额(元)”列重命名为“amount”
    df.rename(columns={'开盘': 'open', '收盘': 'close', '最高': 'high', '最低': 'low', '成交量(股)': 'volume',
                       '成交金额(元)': 'amount'}, inplace=True)
    # 复制一份df，并将复制的df命名为df_copy，保留df_copy中的“datetime”、“open”、“close”、“high”、“low”,“volume”,“amount”列
    df_copy = df[['date', 'open', 'close', 'high', 'low', 'volume', 'amount']].copy()
    return df_copy



if __name__ == '__main__':
    # query_date = '2024-06-11 09:30:00'
    # ndays = 3
    # trade_date = get_trade_date(query_date,ndays)
    # print(trade_date)
    df = get_std_trade_date()
    print(df)

