import argparse
import os
import random
import numpy as np
import torch
import torch.distributed as dist
from exp.exp_long_term_forecasting import Exp_Long_Term_Forecast
from exp.exp_short_term_forecasting import Exp_Short_Term_Forecast
from exp.exp_zero_shot_forecasting import Exp_Zero_Shot_Forecast
from exp.exp_in_context_forecasting import Exp_In_Context_Forecast
from setting import big, get_qwen31
from data_provider.stock import get_all_stocks


class Args:

    def __init__(self):
        self.task_name = 'long_term_forecast'
        self.is_training = 1
        self.model_id = 'stock_800_80'
        self.model = 'AutoTimes_Qwen'
        self.data = 'Stock'
        self.root_path = 'D:/BaiduNetdiskDownload/stock/minute15'
        self.data_path = 'SH.600033'
        self.test_data_path = 'SH.600033'
        self.checkpoints = './checkpoints/'
        self.drop_last = True
        self.val_set_shuffle = True
        self.drop_short = False
        self.seq_len = 800
        self.label_len = 720
        self.token_len = 80
        self.test_seq_len = 800
        self.test_label_len = 720
        self.test_pred_len = 80
        self.seasonal_patterns = 'Monthly'
        self.dropout = 0.1
        qwen31 = get_qwen31(big=big)
        self.llm_ckp_dir = qwen31
        self.mlp_hidden_dim = 256
        self.mlp_hidden_layers = 2
        self.mlp_activation = 'tanh'
        self.num_workers = 10
        self.itr = 1
        self.train_epochs = 2
        self.batch_size = 256
        self.patience = 3
        self.learning_rate = 0.0005
        self.des = 'test'
        self.loss = 'MSE'
        self.lradj = 'type1'
        self.use_amp = True
        self.cosine = True
        self.tmax = 10
        self.weight_decay = 0
        self.mix_embeds = True
        self.test_dir = './test'
        self.test_file_name = 'checkpoint.pth'
        self.gpu = 0
        self.use_multi_gpu = False
        self.visualize = False



def run(stock_code):
    fix_seed = 2021
    random.seed(fix_seed)
    torch.manual_seed(fix_seed)
    np.random.seed(fix_seed)

    args = Args()
    args.data_path = stock_code
    args.test_data_path = stock_code

    if args.use_multi_gpu:
        ip = os.environ.get("MASTER_ADDR", "127.0.0.1")
        port = os.environ.get("MASTER_PORT", "64209")
        hosts = int(os.environ.get("WORLD_SIZE", "8"))
        rank = int(os.environ.get("RANK", "0")) 
        local_rank = int(os.environ.get("LOCAL_RANK", "0"))
        gpus = torch.cuda.device_count()
        args.local_rank = local_rank
        print(ip, port, hosts, rank, local_rank, gpus)
        dist.init_process_group(backend="nccl", init_method=f"tcp://{ip}:{port}", world_size=hosts,
                                rank=rank)
        torch.cuda.set_device(local_rank)
    
    if args.task_name == 'long_term_forecast':
        Exp = Exp_Long_Term_Forecast
    elif args.task_name == 'short_term_forecast':
        Exp = Exp_Short_Term_Forecast
    elif args.task_name == 'zero_shot_forecast':
        Exp = Exp_Zero_Shot_Forecast
    elif args.task_name == 'in_context_forecast':
        Exp = Exp_In_Context_Forecast
    else:
        Exp = Exp_Long_Term_Forecast

    if args.is_training:
        for ii in range(args.itr):
            # setting record of experiments
            exp = Exp(args)  # set experiments
            setting = '{}_{}_{}_{}_sl{}_ll{}_tl{}_lr{}_bt{}_wd{}_hd{}_hl{}_cos{}_mix{}_{}_{}'.format(
                args.task_name,
                args.model_id,
                args.model,
                args.data,
                args.seq_len,
                args.label_len,
                args.token_len,
                args.learning_rate,
                args.batch_size,
                args.weight_decay,
                args.mlp_hidden_dim,
                args.mlp_hidden_layers,
                args.cosine,
                args.mix_embeds,
                args.des, ii)
            if (args.use_multi_gpu and args.local_rank == 0) or not args.use_multi_gpu:
                print('>>>>>>>start training : {}>>>>>>>>>>>>>>>>>>>>>>>>>>'.format(setting))
            exp.train(setting)
            if (args.use_multi_gpu and args.local_rank == 0) or not args.use_multi_gpu:
                print('>>>>>>>testing : {}<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<'.format(setting))
            exp.test(setting)
            torch.cuda.empty_cache()
    else:
        ii = 0
        setting = '{}_{}_{}_{}_sl{}_ll{}_tl{}_lr{}_bt{}_wd{}_hd{}_hl{}_cos{}_mix{}_{}_{}'.format(
            args.task_name,
            args.model_id,
            args.model,
            args.data,
            args.seq_len,
            args.label_len,
            args.token_len,
            args.learning_rate,
            args.batch_size,
            args.weight_decay,
            args.mlp_hidden_dim,
            args.mlp_hidden_layers,
            args.cosine,
            args.mix_embeds,
            args.des, ii)
        exp = Exp(args)  # set experiments
        exp.test(setting, test=1)
        torch.cuda.empty_cache()






if __name__ == '__main__':
    folder = r'D:\BaiduNetdiskDownload\stock\minute15'
    all_stocks = get_all_stocks(folder)
    # 随机调整all_stocks的顺序
    random.shuffle(all_stocks)
    for stock_code in all_stocks:
        run(stock_code)

    
