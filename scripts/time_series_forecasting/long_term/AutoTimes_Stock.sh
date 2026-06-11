model_name=AutoTimes_Qwen

# training one model with a context length
python -u run.py \
  --task_name long_term_forecast \
  --is_training 1 \
  --root_path D:/BaiduNetdiskDownload/stock/minute15 \
  --data_path SH.600033 \
  --model_id stock_800_80 \
  --model $model_name \
  --data Stock \
  --seq_len 800 \
  --label_len 720 \
  --token_len 80 \
  --test_seq_len 800 \
  --test_label_len 720 \
  --test_pred_len 80 \
  --batch_size 256 \
  --learning_rate 0.0005 \
  --mlp_hidden_layers 2 \
  --train_epochs 10 \
  --use_amp \
  --gpu 0 \
  --cosine \
  --tmax 10 \
  --mix_embeds \
  --drop_last

# testing the model on all forecast lengths
for test_pred_len in 80 160 320
do
python -u run.py \
  --task_name long_term_forecast \
  --is_training 0 \
  --root_path D:/BaiduNetdiskDownload/stock/minute15 \
  --data_path SH.600033 \
  --model_id stock_800_80 \
  --model $model_name \
  --data Stock \
  --seq_len 800 \
  --label_len 720 \
  --token_len 80 \
  --test_seq_len 800 \
  --test_label_len 720 \
  --test_pred_len $test_pred_len \
  --batch_size 256 \
  --learning_rate 0.0005 \
  --mlp_hidden_layers 2 \
  --train_epochs 10 \
  --use_amp \
  --gpu 0 \
  --cosine \
  --tmax 10 \
  --mix_embeds \
  --drop_last \
  --test_dir long_term_forecast_stock_800_80_AutoTimes_Qwen_Stock_sl800_ll720_tl80_lr0.0005_bt256_wd0_hd256_hl0_cosTrue_mixTrue_test_0
done
