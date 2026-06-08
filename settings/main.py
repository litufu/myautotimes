import tushare as ts
import pandas as pd



# pro = ts.pro_api(token="f88e93f91c79cdb865f22f40cac23a2907da36b53fa9aa150228ed27")
#
# df = pro.trade_cal(exchange='SSE')
# df.to_csv('trade_cal.csv', index=False)


df = pd.read_csv('trade_cal.csv')
print(df)
df_new = df[df['is_open'] == 1].copy()
# 筛选is_open为1的行
df_new = df_new[df_new['is_open'] == 1]
# 将date从%Y%m%d格式转换为%Y-%m-%d格式
df_new['cal_date'] = pd.to_datetime(df_new['cal_date'], format='%Y%m%d').dt.strftime('%Y-%m-%d')
# 增加一列time列，每天对应增加【9:45 10:00 10:15 10:30 10:45 11:00 11:15 11:30 13:15 13:30 13:45 14:00 14:15 14:30 14:45 15:00】行
df_new['time'] = df_new['cal_date'].apply(lambda x: [f"{x} 09:45:00", f"{x} 10:00:00", f"{x} 10:15:00", f"{x} 10:30:00", f"{x} 10:45:00", f"{x} 11:00:00", f"{x} 11:15:00", f"{x} 11:30:00", f"{x} 13:15:00", f"{x} 13:30:00", f"{x} 13:45:00", f"{x} 14:00:00", f"{x} 14:15:00", f"{x} 14:30:00", f"{x} 14:45:00", f"{x} 15:00:00"])
# 将time列展开成多行
df_new = df_new.explode('time')
df_new.rename(columns={'time': 'date'}, inplace=True)
# df_new保留date列和is_open列
df_new = df_new[['date', 'is_open']]
print(df_new)
df_new.to_csv('stock.csv', index=False)
