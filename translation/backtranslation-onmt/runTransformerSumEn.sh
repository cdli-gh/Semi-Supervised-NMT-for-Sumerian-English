pip3 install OpenNMT-py

echo 'Cloning OpenNMT...'
git clone https://github.com/OpenNMT/OpenNMT-py.git

datadir=${1:-../../../dataset/dataToUse/allCompSents}          # path to directory containing data, refer README for desired data format
savedir=${2:-../../../weights/}       # directory to direct the checkpoints
numGPUs=1         # number of GPUs
gpu_ranks=$numGPUs-1
langPair=${3:-sum-eng}           # source-target
src=$(echo $langPair | cut -d '-' -f 1)
tgt=$(echo $langPair | cut -d '-' -f 2)

datadir2=${4:-../../../dataset/dataToUse/allCompSents}

echo "$datadir, $savedir, $langPair"

cd OpenNMT-py

if [ ! -d "./data/$langPair" ]; then
    mkdir ./data/$langPair
fi

# cp $datadir ./data/$langPair

echo 'Preprocessing Data...'
onmt_preprocess -train_src $datadir/train.$src -train_tgt $datadir/train.$tgt -valid_src $datadir2/dev.$src -valid_tgt $datadir2/dev.$tgt -save_data ./data/$langPair/pped

echo 'Starting Training...'
python3  train.py -data ./data/$langPair/pped -save_model $savedir \
        -layers 6 -rnn_size 512 -word_vec_size 512 -transformer_ff 2048 -heads 8  \
        -encoder_type transformer -decoder_type transformer -position_encoding \
        -train_steps 20000  -max_generator_batches 2 -dropout 0.1 \
        -batch_size 4096 -batch_type tokens -normalization tokens  -accum_count 2 \
        -early_stopping 5 \
        -optim adam -adam_beta2 0.998 -decay_method noam -warmup_steps 8000 -learning_rate 2 \
        -max_grad_norm 0 -param_init 0  -param_init_glorot \
        -label_smoothing 0.1 -valid_steps 1000 -save_checkpoint_steps 1000 \
        -world_size $numGPUs -gpu_ranks 0
