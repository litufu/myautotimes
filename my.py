from data_provider.data_loader import Dataset_ETT_hour




data_set = Dataset_ETT_hour(
    root_path=r'D:\autotimes\dataset\ETT-small',
    data_path='ETTh1.csv',
    flag='train',
    size=[672, 576, 96],
    seasonal_patterns=None,
    drop_short=False,
)
print(data_set[0])