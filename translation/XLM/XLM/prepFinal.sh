dir=$1
dir=$dir/processed/sum-en

cp $dir/train.sum-en.en.pth $dir/train.en-sum.en.pth
cp $dir/train.sum-en.sum.pth $dir/train.en-sum.sum.pth
cp $dir/valid.sum-en.en.pth $dir/valid.en-sum.en.pth
cp $dir/valid.sum-en.sum.pth $dir/valid.en-sum.sum.pth
cp $dir/test.sum-en.en.pth $dir/test.en-sum.en.pth
cp $dir/test.sum-en.sum.pth $dir/test.en-sum.sum.pth
