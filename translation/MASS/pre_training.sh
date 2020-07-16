save_dir=experiments/pre-training/
user_dir=mass
data_dir=data/processed/

mkdir -p $save_dir

fairseq-train $data_dir \
    --user-dir $user_dir \
    --save-dir $save_dir \
    --task xmasked_seq2seq \
    --source-langs en,sum \
    --target-langs en,sum \
    --langs en,sum \
    --arch xtransformer \
    --mass_steps en-en,sum-sum \
    --memt_steps en-sum,sum-en \
    --optimizer adam --adam-betas '(0.9, 0.98)' --clip-norm 0.0 \
    --lr-scheduler inverse_sqrt --lr 0.00005 --min-lr 1e-09 \
    --criterion label_smoothed_cross_entropy \
    --max-tokens 4096 \
    --dropout 0.1 --relu-dropout 0.1 --attention-dropout 0.1 \
    --max-update 100000 \
    --share-decoder-input-output-embed \
    --valid-lang-pairs en-sum \
