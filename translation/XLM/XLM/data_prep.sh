# Copyright (c) 2019-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#

set -e


#
# Data preprocessing configuration
#
N_MONO=5000000  # number of monolingual sentences for each language
CODES=60000     # number of BPE codes
N_THREADS=16    # number of threads in data preprocessing


#
# Read arguments
#
POSITIONAL=()
while [[ $# -gt 0 ]]
do
key="$1"
case $key in
  --src)
    SRC="$2"; shift 2;;
  --tgt)
    TGT="$2"; shift 2;;
  --reload_codes)
    RELOAD_CODES="$2"; shift 2;;
  --reload_vocab)
    RELOAD_VOCAB="$2"; shift 2;;
  *)
  POSITIONAL+=("$1")
  shift
  ;;
esac
done
set -- "${POSITIONAL[@]}"


#
# Check parameters
#
if [ "$SRC" == "" ]; then echo "--src not provided"; exit; fi
if [ "$TGT" == "" ]; then echo "--tgt not provided"; exit; fi
if [ "$SRC" != "de" -a "$SRC" != "en" -a "$SRC" != "fr" -a "$SRC" != "ro" -a "$SRC" != "sum" ]; then echo "unknown source language"; exit; fi
if [ "$TGT" != "de" -a "$TGT" != "en" -a "$TGT" != "fr" -a "$TGT" != "ro" -a "$TGT" != "sum" ]; then echo "unknown target language"; exit; fi
if [ "$SRC" == "$TGT" ]; then echo "source and target cannot be identical"; exit; fi
# if [ "$SRC" \> "$TGT" ]; then echo "please ensure SRC < TGT"; exit; fi
if [ "$RELOAD_CODES" != "" ] && [ ! -f "$RELOAD_CODES" ]; then echo "cannot locate BPE codes"; exit; fi
if [ "$RELOAD_VOCAB" != "" ] && [ ! -f "$RELOAD_VOCAB" ]; then echo "cannot locate vocabulary"; exit; fi
if [ "$RELOAD_CODES" == "" -a "$RELOAD_VOCAB" != "" -o "$RELOAD_CODES" != "" -a "$RELOAD_VOCAB" == "" ]; then echo "BPE codes should be provided if and only if vocabulary is also provided"; exit; fi


#
# Initialize tools and data paths
#
git clone https://github.com/NVIDIA/apex.git

# main paths
MAIN_PATH=$PWD
TOOLS_PATH=$PWD/tools
DATA_PATH=$PWD/data
MONO_PATH=$DATA_PATH/mono
PARA_PATH=$DATA_PATH/para
PROC_PATH=$DATA_PATH/processed/$SRC-$TGT
PROC_PATH1=$DATA_PATH/processed/$TGT-$SRC

# create paths
mkdir -p $TOOLS_PATH
mkdir -p $DATA_PATH
mkdir -p $MONO_PATH
mkdir -p $PARA_PATH
mkdir -p $PROC_PATH

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

# Sennrich's WMT16 scripts for Romanian preprocessing
WMT16_SCRIPTS=$TOOLS_PATH/wmt16-scripts
NORMALIZE_ROMANIAN=$WMT16_SCRIPTS/preprocess/normalise-romanian.py
REMOVE_DIACRITICS=$WMT16_SCRIPTS/preprocess/remove-diacritics.py

# raw and tokenized files
SRC_RAW=$MONO_PATH/$SRC/all.$SRC
TGT_RAW=$MONO_PATH/$TGT/all.$TGT
SRC_TOK=$SRC_RAW.tok
TGT_TOK=$TGT_RAW.tok

# BPE / vocab files
BPE_CODES=$PROC_PATH/codes
SRC_VOCAB=$PROC_PATH/vocab.$SRC
TGT_VOCAB=$PROC_PATH/vocab.$TGT
FULL_VOCAB=$PROC_PATH/vocab.$SRC-$TGT

# train / valid / test monolingual BPE data
SRC_TRAIN_BPE=$PROC_PATH/train.$SRC
TGT_TRAIN_BPE=$PROC_PATH/train.$TGT
SRC_VALID_BPE=$PROC_PATH/valid.$SRC
TGT_VALID_BPE=$PROC_PATH/valid.$TGT
SRC_TEST_BPE=$PROC_PATH/test.$SRC
TGT_TEST_BPE=$PROC_PATH/test.$TGT

# valid / test parallel BPE data
PARA_SRC_VALID_BPE=$PROC_PATH/valid.$SRC-$TGT.$SRC
PARA_TGT_VALID_BPE=$PROC_PATH/valid.$SRC-$TGT.$TGT
PARA_SRC_TEST_BPE=$PROC_PATH/test.$SRC-$TGT.$SRC
PARA_TGT_TEST_BPE=$PROC_PATH/test.$SRC-$TGT.$TGT
PARA_SRC_VALID_BPE1=$PROC_PATH/valid.$TGT-$SRC.$SRC
PARA_TGT_VALID_BPE1=$PROC_PATH/valid.$TGT-$SRC.$TGT
PARA_SRC_TEST_BPE1=$PROC_PATH/test.$TGT-$SRC.$SRC
PARA_TGT_TEST_BPE1=$PROC_PATH/test.$TGT-$SRC.$TGT

# valid / test file raw data
unset PARA_SRC_VALID PARA_TGT_VALID PARA_SRC_TEST PARA_TGT_TEST
if [ "$SRC" == "en" -a "$TGT" == "fr" ]; then
  PARA_SRC_VALID=$PARA_PATH/dev/newstest2013-ref.en
  PARA_TGT_VALID=$PARA_PATH/dev/newstest2013-ref.fr
  PARA_SRC_TEST=$PARA_PATH/dev/newstest2014-fren-ref.en
  PARA_TGT_TEST=$PARA_PATH/dev/newstest2014-fren-ref.fr
fi
if [ "$SRC" == "de" -a "$TGT" == "en" ]; then
  PARA_SRC_VALID=$PARA_PATH/dev/newstest2013-ref.de
  PARA_TGT_VALID=$PARA_PATH/dev/newstest2013-ref.en
  PARA_SRC_TEST=$PARA_PATH/dev/newstest2016-ende-ref.de
  PARA_TGT_TEST=$PARA_PATH/dev/newstest2016-deen-ref.en
  # PARA_SRC_TEST=$PARA_PATH/dev/newstest2014-deen-ref.de
  # PARA_TGT_TEST=$PARA_PATH/dev/newstest2014-deen-ref.en
fi
if [ "$SRC" == "en" -a "$TGT" == "ro" ]; then
  PARA_SRC_VALID=$PARA_PATH/dev/newsdev2016-roen-ref.en
  PARA_TGT_VALID=$PARA_PATH/dev/newsdev2016-enro-ref.ro
  PARA_SRC_TEST=$PARA_PATH/dev/newstest2016-roen-ref.en
  PARA_TGT_TEST=$PARA_PATH/dev/newstest2016-enro-ref.ro
fi
if [ "$SRC" == "sum" -a "$TGT" == "en" ]; then
  PARA_SRC_VALID=$PARA_PATH/dev.sum
  PARA_TGT_VALID=$PARA_PATH/dev.en
  PARA_SRC_TEST=$PARA_PATH/dev.sum
  PARA_TGT_TEST=$PARA_PATH/dev.en
fi

# install tools
./install-tools.sh


#
# Download monolingual data
#

echo "Monolingual Data:"

cd $MONO_PATH

if [ "$SRC" == "sum" -o "$TGT" == "sum" -a ! -f $MONO_PATH/en ]; then
  echo "Copying from dataset directory"
  mkdir -p $MONO_PATH/sum
  cd $MONO_PATH/sum

  cp ../../../../../../dataset/cleaned/UrIIICompSents/mono.sum ./
  cp ../../../../../../dataset/cleaned/allCompSents/mono.sum ./
  cp ../../../../../../dataset/cleaned/allLineByLine/mono.sum ./
fi

if [ "$SRC" == "de" -o "$TGT" == "de" ]; then
  echo "Downloading German monolingual data ..."
  mkdir -p $MONO_PATH/de
  cd $MONO_PATH/de
  wget -c http://www.statmt.org/wmt14/training-monolingual-news-crawl/news.2007.de.shuffled.gz
  wget -c http://www.statmt.org/wmt14/training-monolingual-news-crawl/news.2008.de.shuffled.gz

if [ "$SRC" == "en" -o "$TGT" == "en" -a ! -f $MONO_PATH/en ]; then
  echo "Downloading English monolingual data ..."
  mkdir -p $MONO_PATH/en
  cd $MONO_PATH/en
  wget -c http://www.statmt.org/wmt14/training-monolingual-news-crawl/news.2007.en.shuffled.gz
  wget -c http://www.statmt.org/wmt14/training-monolingual-news-crawl/news.2008.en.shuffled.gz
fi

if [ "$SRC" == "fr" -o "$TGT" == "fr" ]; then
  echo "Downloading French monolingual data ..."
  mkdir -p $MONO_PATH/fr
  cd $MONO_PATH/fr
  wget -c http://www.statmt.org/wmt14/training-monolingual-news-crawl/news.2007.fr.shuffled.gz
  wget -c http://www.statmt.org/wmt14/training-monolingual-news-crawl/news.2008.fr.shuffled.gz
  wget -c http://www.statmt.org/wmt14/training-monolingual-news-crawl/news.2009.fr.shuffled.gz
fi

if [ "$SRC" == "ro" -o "$TGT" == "ro" ]; then
  echo "Downloading Romanian monolingual data ..."
  mkdir -p $MONO_PATH/ro
  cd $MONO_PATH/ro
  wget -c http://data.statmt.org/wmt16/translation-task/news.2015.ro.shuffled.gz
fi

cd $MONO_PATH

# decompress monolingual data
if [ $SRC != "sum" ]; then
  for FILENAME in $SRC/news*gz; do
    OUTPUT="${FILENAME::-3}"
    if [ ! -f "$OUTPUT"]; then
      echo "Decompressing $FILENAME..."
      gunzip -k $FILENAME
    else
      echo "$OUTPUT already decompressed."
    fi
  done
fi

for FILENAME in $TGT/news*gz; do
  OUTPUT="${FILENAME::-3}"
  if [ ! -f "$OUTPUT"]; then
    echo "Decompressing $FILENAME..."
    gunzip -k $FILENAME
  else
    echo "$OUTPUT already decompressed."
  fi
done

# concatenate monolingual data files
if [$SRC == "sum"]; then
  python3 ../stack.py --src $SRC/ --tgt $SRC/all.sum
fi

if [$TGT == "eng"]; then
  python3 ../stack.py --src $TGT/ --tgt $TGT/all.eng
fi

if ! [[ -f "$TGT_RAW" ]]; then
  echo "Concatenating $TGT monolingual data..."
  cat $(ls $TGT/news*$TGT* | grep -v gz) | head -n $N_MONO > $TGT_RAW
fi
echo "$SRC monolingual data concatenated in: $SRC_RAW"
echo "$TGT monolingual data concatenated in: $TGT_RAW"

# preprocessing commands - special case for Romanian
if [ "$SRC" == "ro" ]; then
  SRC_PREPROCESSING="$REPLACE_UNICODE_PUNCT | $NORM_PUNC -l $SRC | $REM_NON_PRINT_CHAR | $NORMALIZE_ROMANIAN | $REMOVE_DIACRITICS | $TOKENIZER -l $SRC -no-escape -threads $N_THREADS"
else
  SRC_PREPROCESSING="$REPLACE_UNICODE_PUNCT | $NORM_PUNC -l $SRC | $REM_NON_PRINT_CHAR |                                            $TOKENIZER -l $SRC -no-escape -threads $N_THREADS"
fi
if [ "$TGT" == "ro" ]; then
  TGT_PREPROCESSING="$REPLACE_UNICODE_PUNCT | $NORM_PUNC -l $TGT | $REM_NON_PRINT_CHAR | $NORMALIZE_ROMANIAN | $REMOVE_DIACRITICS | $TOKENIZER -l $TGT -no-escape -threads $N_THREADS"
else
  TGT_PREPROCESSING="$REPLACE_UNICODE_PUNCT | $NORM_PUNC -l $TGT | $REM_NON_PRINT_CHAR |                                            $TOKENIZER -l $TGT -no-escape -threads $N_THREADS"
fi

# tokenize data
if ! [[ -f "$SRC_TOK" ]]; then
  echo "Tokenize $SRC monolingual data..."
  eval "cat $SRC_RAW | $SRC_PREPROCESSING > $SRC_TOK"
fi

if ! [[ -f "$TGT_TOK" ]]; then
  echo "Tokenize $TGT monolingual data..."
  eval "cat $TGT_RAW | $TGT_PREPROCESSING > $TGT_TOK"
fi
echo "$SRC monolingual data tokenized in: $SRC_TOK"
echo "$TGT monolingual data tokenized in: $TGT_TOK"

# reload BPE codes
cd $MAIN_PATH
if [ ! -f "$BPE_CODES" ] && [ -f "$RELOAD_CODES" ]; then
  echo "Reloading BPE codes from $RELOAD_CODES ..."
  cp $RELOAD_CODES $BPE_CODES
fi

# learn BPE codes
if [ ! -f "$BPE_CODES" ]; then
  echo "Learning BPE codes..."
  $FASTBPE learnbpe $CODES $SRC_TOK $TGT_TOK > $BPE_CODES
fi
echo "BPE learned in $BPE_CODES"

# apply BPE codes
if ! [[ -f "$SRC_TRAIN_BPE" ]]; then
  echo "Applying $SRC BPE codes..."
  $FASTBPE applybpe $SRC_TRAIN_BPE $SRC_TOK $BPE_CODES
fi
if ! [[ -f "$TGT_TRAIN_BPE" ]]; then
  echo "Applying $TGT BPE codes..."
  $FASTBPE applybpe $TGT_TRAIN_BPE $TGT_TOK $BPE_CODES
fi
echo "BPE codes applied to $SRC in: $SRC_TRAIN_BPE"
echo "BPE codes applied to $TGT in: $TGT_TRAIN_BPE"

# extract source and target vocabulary
if ! [[ -f "$SRC_VOCAB" && -f "$TGT_VOCAB" ]]; then
  echo "Extracting vocabulary..."
  $FASTBPE getvocab $SRC_TRAIN_BPE > $SRC_VOCAB
  $FASTBPE getvocab $TGT_TRAIN_BPE > $TGT_VOCAB
fi
echo "$SRC vocab in: $SRC_VOCAB"
echo "$TGT vocab in: $TGT_VOCAB"

# reload full vocabulary
cd $MAIN_PATH
if [ ! -f "$FULL_VOCAB" ] && [ -f "$RELOAD_VOCAB" ]; then
  echo "Reloading vocabulary from $RELOAD_VOCAB ..."
  cp $RELOAD_VOCAB $FULL_VOCAB
fi

# extract full vocabulary
if ! [[ -f "$FULL_VOCAB" ]]; then
  echo "Extracting vocabulary..."
  $FASTBPE getvocab $SRC_TRAIN_BPE $TGT_TRAIN_BPE > $FULL_VOCAB
fi
echo "Full vocab in: $FULL_VOCAB"

# binarize data
if ! [[ -f "$SRC_TRAIN_BPE.pth" ]]; then
  echo "Binarizing $SRC data..."
  $MAIN_PATH/preprocess.py $FULL_VOCAB $SRC_TRAIN_BPE
fi
if ! [[ -f "$TGT_TRAIN_BPE.pth" ]]; then
  echo "Binarizing $TGT data..."
  $MAIN_PATH/preprocess.py $FULL_VOCAB $TGT_TRAIN_BPE
fi
echo "$SRC binarized data in: $SRC_TRAIN_BPE.pth"
echo "$TGT binarized data in: $TGT_TRAIN_BPE.pth"


#
# Download parallel data (for evaluation only)
#

cd $PARA_PATH

if [ "$SRC" == "sum" ]; then
    cp ../../../../../dataset/dataToUse/UrIIICompSents/dev.sum ./dev.sum.sgm
    cp ../../../../../dataset/dataToUse/allCompSents/dev.eng ./dev.en.sgm
else
    echo "Downloading parallel data..."
    wget -c http://data.statmt.org/wmt18/translation-task/dev.tgz

    echo "Extracting parallel data..."
    tar -xzf dev.tgz
fi

# check valid and test files are here
if ! [[ -f "$PARA_SRC_VALID.sgm" ]]; then echo "$PARA_SRC_VALID.$SRC is not found!"; exit; fi
if ! [[ -f "$PARA_TGT_VALID.sgm" ]]; then echo "$PARA_TGT_VALID.$TGT is not found!"; exit; fi
if ! [[ -f "$PARA_SRC_TEST.sgm" ]];  then echo "$PARA_SRC_TEST.$SRC is not found!";  exit; fi
if ! [[ -f "$PARA_TGT_TEST.sgm" ]];  then echo "$PARA_TGT_TEST.$TGT is not found!";  exit; fi

echo "Tokenizing valid and test data..."
eval "cat $PARA_SRC_VALID.sgm | $SRC_PREPROCESSING > $PARA_SRC_VALID"
eval "cat $PARA_TGT_VALID.sgm | $TGT_PREPROCESSING > $PARA_TGT_VALID"
eval "cat $PARA_SRC_TEST.sgm | $SRC_PREPROCESSING > $PARA_SRC_TEST"
eval "cat $PARA_TGT_TEST.sgm | $TGT_PREPROCESSING > $PARA_TGT_TEST"

echo "Applying BPE to valid and test files..."
$FASTBPE applybpe $PARA_SRC_VALID_BPE $PARA_SRC_VALID $BPE_CODES $SRC_VOCAB
$FASTBPE applybpe $PARA_TGT_VALID_BPE $PARA_TGT_VALID $BPE_CODES $TGT_VOCAB
$FASTBPE applybpe $PARA_SRC_TEST_BPE  $PARA_SRC_TEST  $BPE_CODES $SRC_VOCAB
$FASTBPE applybpe $PARA_TGT_TEST_BPE  $PARA_TGT_TEST  $BPE_CODES $TGT_VOCAB
$FASTBPE applybpe $PARA_SRC_VALID_BPE1 $PARA_SRC_VALID $BPE_CODES $SRC_VOCAB
$FASTBPE applybpe $PARA_TGT_VALID_BPE1 $PARA_TGT_VALID $BPE_CODES $TGT_VOCAB
$FASTBPE applybpe $PARA_SRC_TEST_BPE1 $PARA_SRC_TEST  $BPE_CODES $SRC_VOCAB
$FASTBPE applybpe $PARA_TGT_TEST_BPE1 $PARA_TGT_TEST  $BPE_CODES $TGT_VOCAB

echo "Binarizing data..."
rm -f $PARA_SRC_VALID_BPE.pth $PARA_TGT_VALID_BPE.pth $PARA_SRC_TEST_BPE.pth $PARA_TGT_TEST_BPE.pth
python3 $MAIN_PATH/preprocess.py $FULL_VOCAB $PARA_SRC_VALID_BPE
python3 $MAIN_PATH/preprocess.py $FULL_VOCAB $PARA_TGT_VALID_BPE
python3 $MAIN_PATH/preprocess.py $FULL_VOCAB $PARA_SRC_TEST_BPE
python3 $MAIN_PATH/preprocess.py $FULL_VOCAB $PARA_TGT_TEST_BPE


#
# Link monolingual validation and test data to parallel data
#
ln -sf $PARA_SRC_VALID_BPE.pth $SRC_VALID_BPE.pth
ln -sf $PARA_TGT_VALID_BPE.pth $TGT_VALID_BPE.pth
ln -sf $PARA_SRC_TEST_BPE.pth  $SRC_TEST_BPE.pth
ln -sf $PARA_TGT_TEST_BPE.pth  $TGT_TEST_BPE.pth


#
# Summary
#
echo ""
echo "===== Data summary"
echo "Monolingual training data:"
echo "    $SRC: $SRC_TRAIN_BPE.pth"
echo "    $TGT: $TGT_TRAIN_BPE.pth"
echo "Monolingual validation data:"
echo "    $SRC: $SRC_VALID_BPE.pth"
echo "    $TGT: $TGT_VALID_BPE.pth"
echo "Monolingual test data:"
echo "    $SRC: $SRC_TEST_BPE.pth"
echo "    $TGT: $TGT_TEST_BPE.pth"
echo "Parallel validation data:"
echo "    $SRC: $PARA_SRC_VALID_BPE.pth"
echo "    $TGT: $PARA_TGT_VALID_BPE.pth"
echo "Parallel test data:"
echo "    $SRC: $PARA_SRC_TEST_BPE.pth"
echo "    $TGT: $PARA_TGT_TEST_BPE.pth"
echo ""
