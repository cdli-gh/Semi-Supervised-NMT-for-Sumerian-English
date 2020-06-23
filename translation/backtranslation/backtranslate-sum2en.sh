cd fairseq

ulimit -n 4096

srclang=$1
tgtlang=$2
CHECKPOINT_DIR=$3

fairseq-train --fp16 \
    data-bin/sum_en \
    --source-lang $srclang --target-lang $tgtlang \
    --arch transformer_wmt_en_de_big --share-all-embeddings \
    --dropout 0.3 --weight-decay 0.0 \
    --criterion label_smoothed_cross_entropy --label-smoothing 0.1 \
    --optimizer adam --adam-betas '(0.9, 0.98)' --clip-norm 0.0 \
    --lr 0.001 --lr-scheduler inverse_sqrt --warmup-updates 4000 \
    --max-tokens 2048 --update-freq 2 \
    --max-update 30000 \
    --save-dir $CHECKPOINT_DIR \
    # --restore-file $CHECKPOINT_DIR/checkpoint4.pt \
    # --pretrained-checkpoint $CHECKPOINT_DIR/checkpoint_last.pt
