cd fairseq
TEXT=../../../dataset/mixed
fairseq-preprocess \
    --joined-dictionary \
    --source-lang eng --target-lang sum \
    --trainpref $TEXT/train --validpref $TEXT/dev --testpref $TEXT/test \
    --destdir data-bin/sum_en --thresholdtgt 0 --thresholdsrc 0 \
    --workers 20