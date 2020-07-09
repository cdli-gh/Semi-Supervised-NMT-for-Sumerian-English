# Transformer for Sumerian-English NMT

## Pre-Trained Checkpoint

To load a pre-trained checkpoint, run the following command in the appropriate directory:

```
wget https://cdlisumerianunmt.s3.us-east-2.amazonaws.com/Transformer/AllCompSents/_step_14000.pt
```

Path to this directory you be mentioned in the ```Translating``` part below.

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
