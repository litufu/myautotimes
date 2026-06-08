import pathlib
import pandas as pd

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

if __name__ == '__main__':
    # query_date = '2024-06-11 09:30:00'
    # ndays = 3
    # trade_date = get_trade_date(query_date,ndays)
    # print(trade_date)
    df = get_std_trade_date()
    print(df)

