data_dir=data/processed
save_dir=experiments/fine-tuning/
user_dir=mass
model=experiments/pre-training/checkpoint_last.pt # The path of pre-trained model

mkdir -p $save_dir

fairseq-train $data_dir \
    --user-dir $user_dir \
    --task xmasked_seq2seq \
    --source-langs sum --target-langs en \
    --langs sum,en \
    --arch xtransformer \
    --mt_steps sum-en \
    --save-dir $save_dir \
    --optimizer adam --adam-betas '(0.9, 0.98)' --clip-norm 0.0 \
    --lr-scheduler inverse_sqrt --lr-shrink 0.5 --lr 0.00005 --min-lr 1e-09 \
    --criterion label_smoothed_cross_entropy \
    --max-tokens 4096 \
    --max-update 100000 --max-epoch 50 \
    --dropout 0.1 --relu-dropout 0.1 --attention-dropout 0.1 \
    --share-decoder-input-output-embed \
    --valid-lang-pairs sum-en \
    --reload_checkpoint $model
