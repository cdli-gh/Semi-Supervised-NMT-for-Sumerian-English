# XLM

## For Training:

### Prepare your Training Data

```
sh data_prep_2.sh --src sum --tgt en

sh prepFinal.sh data2
```

### Pre-Training

#### Using MLM 

```
python3 train.py --exp_name <experiment_name> \
                --dump_path <weights_save_dir> \
                --data_path ./data2/processed/sum-en/ \
                --lgs 'sum-en' --mlm_steps 'sum,en' \
                --validation_metrics _valid_mlm_ppl \
                --stopping_criterion _valid_mlm_ppl,10
```

#### Using TLM 

add  ```sum-en``` inside ```--mlm_steps ' '```

#### Using CLM

add ```--clm_steps 'sum,en'```

### Second Phase of Training

#### Unsupervised:

```
python3 train.py --exp_name <experiment_name> \
                --dump_path <weights_save_dir> \
                --reload_model <weights_save_dir>/<folder_name>/checkpoint.pth,<weights_save_dir>/<folder_name>/checkpoint.pth'
                --data_path ./data2/processed/sum-en/ \
                --lgs 'sum-en' --ae_steps 'sum,en' --bt_steps 'sum-en-sum,en-sum-en' \
                --word_shuffle 3 --word_dropout 0.1 --word_blank 0.1 \
                --encoder_only false \
                --tokens_per_batch 2000 --eval_bleu true \
                --validation_metrics 'valid_sum-en_mt_bleu' \
                --stopping_criterion 'valid_sum-en_mt_bleu,10'
```

#### Semi-Supervised:

```
python3 train.py --exp_name <experiment_name> \
                --dump_path <weights_save_dir> \
                --reload_model <weights_save_dir>/<folder_name>/checkpoint.pth,<weights_save_dir>/<folder_name>/checkpoint.pth'
                --data_path ./data2/processed/sum-en/ \
                --lgs 'sum-en' --mt_steps 'sum-en' --bt_steps 'sum-en-sum,en-sum-en' \
                --encoder_only false \
                --tokens_per_batch 2000 --eval_bleu true \
                --validation_metrics 'valid_sum-en_mt_bleu' \
                --stopping_criterion 'valid_sum-en_mt_bleu,10'
```

## For Inference:

### Prepare Data to Test on

```
sh inferPre.sh <SRC_LANG> \
               <SRC_PATH> \
               <BPE_CODES> \
               <RELOAD_VOCAB> \
               <SAVE_DIR>
```

### Run model

```
cat <SAVE_DIR>/evaluate.<SRC_LANG>.bpe | \
        python translate.py --exp_name <experiment_name> \
        --src_lang sum --tgt_lang en \
        --model_path ../<weights_save_dir>/checkpoint.pth --output_path <output_dir>
```

## References:
- [Cross-lingual Language Model Pretraining](https://arxiv.org/abs/1901.07291)
- [Unsupervised Cross-lingual Representation Learning at Scale](https://arxiv.org/abs/1911.02116)
- [XLM GitHub Repository](https://github.com/facebookresearch/XLM)
