# Ensure the output directory exists
data_dir=data
mono_data_dir=$data_dir/mono
para_data_dir=$data_dir/para
save_dir=$data_dir/processed

# set this relative path of MASS in your server
user_dir=mass

mkdir -p $save_dir

# Generate Monolingual Data
echo "Monolingual Data Prep:"
for lg in sum en
do

  fairseq-preprocess \
  --task cross_lingual_lm \
  --srcdict $mono_data_dir/dict.$lg.txt \
  --only-source \
  --trainpref $mono_data_dir/train --validpref $mono_data_dir/valid \
  --destdir $save_dir \
  --workers 20 \
  --source-lang $lg

  # Since we only have a source language, the output file has a None for the
  # target language. Remove this

  echo "Preprocess Done, now moving"

  for stage in train valid
  do
    mv $save_dir/$stage.$lg-None.$lg.bin $save_dir/$stage.$lg.bin
    mv $save_dir/$stage.$lg-None.$lg.idx $save_dir/$stage.$lg.idx
  done
done

# Generate Bilingual Data
fairseq-preprocess \
  --user-dir $user_dir \
  --task xmasked_seq2seq \
  --source-lang sum --target-lang en \
  --trainpref $para_data_dir/train --validpref $para_data_dir/valid \
  --destdir $save_dir \
  --srcdict $para_data_dir/dict.sum.txt \
  --tgtdict $para_data_dir/dict.en.txt

  fairseq-preprocess \
    --user-dir $user_dir \
    --task xmasked_seq2seq \
    --source-lang en --target-lang sum \
    --trainpref $para_data_dir/train --validpref $para_data_dir/valid \
    --destdir $save_dir \
    --srcdict $para_data_dir/dict.sum.txt \
    --tgtdict $para_data_dir/dict.en.txt
