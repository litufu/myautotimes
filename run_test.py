import pandas as pd
import sqlite3
import os
from run_func import predict,get_model
import tushare as ts
from settings.utils import get_std_stock,get_trade_date


pro = ts.pro_api("50e288c10fe08910ea98c8ca7c6a78ff6a36fe6fdab8678f28d5e70d")
model,args,device = get_model()
engine = sqlite3.connect('test.db')
dir = r"D:\BaiduNetdiskDownload\stock\minute15"
# 获取dir下面所有的子目录
dir_children = [d for d in os.listdir(dir) if os.path.isdir(os.path.join(dir, d))]

df_trade_cal = pro.trade_cal(exchange='SSE', start_date='20220401', end_date='20260101')
df_trade_cal.sort_values(by='cal_date', inplace=True)
df_trade_cal = df_trade_cal[df_trade_cal['is_open'] == 1]
df_trade_cal.reset_index(drop=True, inplace=True)


for index, row in df_trade_cal.iterrows():
    trade_date = row['cal_date']
    predict_date_start = df_trade_cal["cal_date"].iloc[index+1]  # 获取trade_date对应的前1个交易日
    predict_date_start = pd.to_datetime(predict_date_start).strftime('%Y-%m-%d')
    predict_date_end = df_trade_cal["cal_date"].iloc[index+5]  # 获取trade_date对应的前5个交易日
    predict_date_end = pd.to_datetime(predict_date_end).strftime('%Y-%m-%d')
    # 将日期转换为字符串格式
    trade_date_str = str(trade_date)
    # 将日期字符串转换为标准格式
    test_date = pd.to_datetime(trade_date_str).strftime('%Y-%m-%d')
    test_year = test_date.split('-')[0]
    while True:
        if test_year in dir_children:
            child_path = os.path.join(dir, test_year)
            # 获取child_path下面所有的csv文件
            csv_files = [f for f in os.listdir(child_path) if f.endswith('.csv')]
            for csv_file in csv_files:
                file_path = os.path.join(child_path, csv_file)
                df_stock = pd.read_csv(file_path)
                select_test_date = df_stock[df_stock['日期'] == test_date]
                if select_test_date.empty:
                    continue
                test_date_index = select_test_date.index.max()
                test_date_close = select_test_date['收盘'].values[-1]
                df_actual = df_stock[(df_stock['日期'] >= predict_date_start)&(df_stock['日期'] <= predict_date_end) ]
                actual_close = df_actual['收盘'].values[-1]
                actual_open = df_actual['开盘'].values[0]
                actual_high = df_actual['最高'].max()
                actual_low = df_actual['最低'].min()

                df_stock_new = get_std_stock(df_stock)
                past_days = [160, 240, 320, 400, 480, 560, 640, 720]

                for past_day in past_days:
                    if test_date_index - past_day < 0:
                        continue
                    df_temp = df_stock_new.iloc[test_date_index - past_day+1:test_date_index + 1].copy()
                    print(f"Processing stock: {csv_file.replace('.csv', '')}, test_date: {test_date}, past_day: {past_day}")
                    print(df_temp)
                    df_res = predict(df_temp, model,args,device,past_day)
                    predict_open = df_res["open"].iloc[0]
                    predict_high = df_res["high"].max()
                    predict_low = df_res["low"].min()
                    predict_close = df_res["close"].iloc[-1]

                    res = {
                        "stock_code": [csv_file.replace(".csv", "")],
                        "test_date": [test_date],
                        "predict_date_start": [predict_date_start],
                        "predict_date_end": [predict_date_end],
                        "test_date_close": [test_date_close],
                        "past_day": [past_day],
                        "predict_open": [predict_open],
                        "predict_high": [predict_high],
                        "predict_low": [predict_low],
                        "predict_close": [predict_close],
                        "actual_open": [actual_open],
                        "actual_high": [actual_high],
                        "actual_low": [actual_low],
                        "actual_close": [actual_close],

                    }
                    df_res_temp = pd.DataFrame(res)
                    df_res_temp.to_sql('predict_results', engine, if_exists='append', index=False)






