#!/bin/bash

cd fairseq

SCRIPTS=mosesdecoder/scripts
TOKENIZER=$SCRIPTS/tokenizer/tokenizer.perl
NORM_PUNC=$SCRIPTS/tokenizer/normalize-punctuation.perl
REM_NON_PRINT_CHAR=$SCRIPTS/tokenizer/remove-non-printing-char.perl
BPEROOT=subword-nmt/subword_nmt


BPE_CODE=sum_en/code
SUBSAMPLE_SIZE=1000000
LANG=sum


OUTDIR=${LANG}_mono
orig=orig
tmp=$OUTDIR/tmp
datadir=$1

mkdir -p $OUTDIR $tmp

CORPORA=(
    'mono'
)

rm $tmp/train.tags.$lang.tok.$l
for f in "${CORPORA[@]}"; do
    cp $datadir/$f.$LANG $orig/$f.$LANG
done

echo "Loaded Data"

if [ -f $tmp/monolingual.${SUBSAMPLE_SIZE}.${LANG} ]; then
    echo "found monolingual sample, skipping shuffle/sample/tokenize"
else
    shuf -n $SUBSAMPLE_SIZE $(for f in "${CORPORA[@]}"; do echo $orig/$f.$LANG; done) \
    | perl $NORM_PUNC $LANG \
    | perl $REM_NON_PRINT_CHAR \
    | perl $TOKENIZER -threads 8 -a -l $LANG \
    > $tmp/monolingual.${SUBSAMPLE_SIZE}.${LANG}
fi

echo "Step 1 Done"

if [ -f $tmp/bpe.monolingual.${SUBSAMPLE_SIZE}.${LANG} ]; then
    echo "found BPE monolingual sample, skipping BPE step"
else
    python $BPEROOT/apply_bpe.py -c $BPE_CODE \
        < $tmp/monolingual.${SUBSAMPLE_SIZE}.${LANG} \
        > $tmp/bpe.monolingual.${SUBSAMPLE_SIZE}.${LANG}
fi

echo "Step 2 Done"

if [ -f $tmp/bpe.monolingual.dedup.${SUBSAMPLE_SIZE}.${LANG} ]; then
    echo "found deduplicated monolingual sample, skipping deduplication step"
else
    python3 ./examples/backtranslation/deduplicate_lines.py $tmp/bpe.monolingual.${SUBSAMPLE_SIZE}.${LANG} \
    > $tmp/bpe.monolingual.dedup.${SUBSAMPLE_SIZE}.${LANG}
fi

echo "Step 3 Done"

if [ -f $OUTDIR/bpe.monolingual.dedup.00.sum ]; then
    echo "found sharded data, skipping sharding step"
else
    split --lines 200000 --numeric-suffixes \
        --additional-suffix .${LANG} \
        $tmp/bpe.monolingual.dedup.${SUBSAMPLE_SIZE}.${LANG} \
        $OUTDIR/bpe.monolingual.dedup.
fi


for SHARD in $(seq -f "%02g" 0 24); do \
    fairseq-preprocess \
        --only-source \
        --source-lang eng --target-lang sum \
        --joined-dictionary \
        --srcdict data-bin/wmt18_en_de/dict.de.txt \
        --testpref $/bpe.monolingual.dedup.${SHARD} \
        --destdir data-bin/wmt18_de_mono/shard${SHARD} \
        --workers 20; \
    cp data-bin/wmt18_en_de/dict.en.txt data-bin/wmt18_de_mono/shard${SHARD}/; \
done

echo "DONE"
