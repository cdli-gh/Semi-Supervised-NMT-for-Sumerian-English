set -e

N_MONO=5000000  # number of monolingual sentences for each language
CODES=60000     # number of BPE codes
N_THREADS=16    # number of threads in data preprocessing

SRC=$1
SRC_PATH=$2
RELOAD_CODES=$3
RELOAD_VOCAB=$4
OUT=$5

if [ "$SRC" == "" ]; then echo "--src not provided"; exit; fi
if [ "$RELOAD_CODES" != "" ] && [ ! -f "$RELOAD_CODES" ]; then echo "cannot locate BPE codes"; exit; fi
if [ "$RELOAD_VOCAB" != "" ] && [ ! -f "$RELOAD_VOCAB" ]; then echo "cannot locate vocabulary"; exit; fi
if [ "$RELOAD_CODES" == "" -a "$RELOAD_VOCAB" != "" -o "$RELOAD_CODES" != "" -a "$RELOAD_VOCAB" == "" ]; then echo "BPE codes should be provided if and only if vocabulary is also provided"; exit; fi

# main paths
MAIN_PATH=$PWD
TOOLS_PATH=$PWD/tools
PROC_PATH=$OUT

# moses
MOSES=$TOOLS_PATH/mosesdecoder
REPLACE_UNICODE_PUNCT=$MOSES/scripts/tokenizer/replace-unicode-punctuation.perl
NORM_PUNC=$MOSES/scripts/tokenizer/normalize-punctuation.perl
REM_NON_PRINT_CHAR=$MOSES/scripts/tokenizer/remove-non-printing-char.perl
TOKENIZER=$MOSES/scripts/tokenizer/tokenizer.perl
INPUT_FROM_SGM=$MOSES/scripts/ems/support/input-from-sgm.perl

# fastBPE
FASTBPE_DIR=$TOOLS_PATH/fastBPE
FASTBPE=$TOOLS_PATH/fastBPE/fast

# raw and tokenized files
cp $SRC_PATH $OUT/temp.$SRC

SRC_RAW=$OUT/temp.$SRC
SRC_TOK=$SRC_RAW.tok

# BPE / vocab files
BPE_CODES=$RELOAD_CODES
SRC_VOCAB=$RELOAD_VOCAB

# valid / test parallel BPE data
SRC_TRAIN_BPE=$OUT/temp.$SRC.bpe

echo "Preprocessing:"

SRC_PREPROCESSING="$REPLACE_UNICODE_PUNCT | $NORM_PUNC -l $SRC | $REM_NON_PRINT_CHAR | $TOKENIZER -l $SRC -no-escape -threads $N_THREADS"

# tokenize data
if ! [[ -f "$SRC_TOK" ]]; then
  echo "Tokenize $SRC monolingual data..."
  eval "cat $SRC_RAW | $SRC_PREPROCESSING > $SRC_TOK"
fi

echo "$SRC tokenized in: $SRC_TOK"

cd $MAIN_PATH

# apply BPE codes
if ! [[ -f "$SRC_TRAIN_BPE" ]]; then
  echo "Applying $SRC BPE codes..."
  $FASTBPE applybpe $SRC_TRAIN_BPE $SRC_TOK $BPE_CODES
fi
