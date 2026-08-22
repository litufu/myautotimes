qwen35 = "./Qwen3-5___7B-Base"

# 千问3是1的7B版本，千问3是0的6B版本。big=True表示使用千问3是1的7B版本，big=False表示使用千问3是0的6B版本。
big = True

# 数据集,存储嵌入日期对应的pt
dataset_path = "./dataset/"

def get_qwen31(big=False):
    if big:
        qwen31 = "./Qwen3-1___7B-Base"
    else:
        qwen31 = "./Qwen3-0___6B"

    return qwen31


