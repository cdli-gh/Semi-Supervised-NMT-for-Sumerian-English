# Transformer for Sumerian-English NMT

## Pre-Trained Checkpoint

We have trained the Vanilla Transformer model for 4 data configurations as mentioned before and provide weights for all four of them. Replace ```data_mode``` ```[AllCompSents, UrIIICompSents, UrIIILineByLine, AllLineByLine]``` in the following command to load the respective pre-trained checkpoint:

```
wget https://cdlisumerianunmt.s3.us-east-2.amazonaws.com/Transformer/<data_mode>/_step_14000.pt
```

Path to this directory needs to be mentioned while [Translating](https://github.com/cdli-gh/Unsupervised-NMT-for-Sumerian-English/blob/master/translation/transformer/README.md#translating).

## Training

```
sh runTransformerSumEn.sh <datadir, path to data directory> <savedir, path to directory where the model weights are to be stored> <langPair, source-target languages, if training for any other language pairs>
```

#### Default arguments:

- ```<datadir>``` is set to the ```dataset/allCompSents``` folder (refer to the documentation in the dataset folder to know the details) <br>
- ```<savedir>``` is set to the ```savedWeights``` folder <br>
- ```<langPair>``` is set to 'sum-eng' <br>

## Translating 

```
onmt_translate -model <path to the saved the model> -src <path to the data to be translated> -output <path to the output text file> -replace_unk -verbose
```

#### Sample arguments:
- model: ```../../savedWeights/_step_20000.pt``` 
- src: ```../../dataset/dataToUse/UrIIICompSents/test.sum``` 
- output: ```../../results/pred_eng.txt```
- verbose: 0 (if you don't wish to print the outputs while they are evaluated)
