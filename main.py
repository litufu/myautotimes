import os
import tushare as ts
import torch



# ts.set_token('f88e93f91c79cdb865f22f40cac23a2907da36b53fa9aa150228ed27')
# pro = ts.pro_api()
# df = pro.query('trade_cal', start_date='20261231', end_date='20271231')
# print(df)

data_stamp = torch.load(r"D:\autotimes\dataset\stock.pt")
print(data_stamp)
print(data_stamp.shape)
# reversed_list = data_stamp[::-1]
data_stamp = reversed(data_stamp)

torch.save(data_stamp, r"D:\autotimes\dataset\stock_reversed.pt")
print(data_stamp)


     
