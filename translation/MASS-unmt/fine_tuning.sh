MODEL=dumped/unsupMT_sumen/1079444/checkpoint.pth

python train.py \
  --exp_name unsupMT_sumen_FT                              \
  --data_path ./data/processed/sum-en/                  \
  --lgs 'en-sum'                                        \
  --bt_steps 'en-sum-en,sum-en-sum'                       \
  --encoder_only false                                 \
  --emb_dim 1024                                       \
  --n_layers 6                                         \
  --n_heads 8                                          \
  --dropout 0.1                                        \
  --attention_dropout 0.1                              \
  --gelu_activation true                               \
  --tokens_per_batch 2000                              \
  --batch_size 32	                                     \
  --bptt 256                                           \
  --optimizer adam_inverse_sqrt,beta1=0.9,beta2=0.98,lr=0.0001 \
  --epoch_size 200000                                  \
  --max_epoch 30                                       \
  --eval_bleu true                                     \
  --reload_model "$MODEL,$MODEL"                       \
