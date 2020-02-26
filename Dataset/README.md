# Dataset Description

## Original Dataset
This is Original data provided by organization. Dataset contains short phrases, data is noisy, repetitive phrases, there are some missing phrases too denoted by "xxxx".

As a developer feel free to experiment with this dataset, such as applying own augmentation algorithms,  probably learning embeddings from external corpora to augment the translation performance of the models. etc.

**sum_eng_train.csv:** File contains 16017 Sumerian and English language pairs.

**sum_eng_test.csv:** File contains 1933 Sumerian and English language pairs.

**sum_eng_develop.csv:** File contains 2059 Sumerian and English language pairs.

As the name suggests train file can be used for training model, Final performance of the model should be on test files.
Develop file are standard development file. Can be used for hyperparameter tuning and evaluation. Can also be used as a validation set.

.txt files are same dataset parallel phrases in another file format.
Some redundant phrases were removed from CVS files, so you may observe that they have fewer phrases that .csv files.

## Cleaned Dataset

This data is derived using the Original Dataset. While cleaning dataset, repetitive and missing phrases are removed. Cleaned Data set is only available as .txt files.

**train files:** Contains 8117 phrase.

**test files:** Contains 1015 phrases.

**val files:** Contains 1015 phrases.

## Normalized dataset
This dataset is derived from Cleaned dataset. While process of normalization
1. All characters are reduced to lower case,
2. Punctuation are removed from both Sumerian and English files.
3. Stop Words removed from English files. Sumerian don't have stop words.

This is done to remove redundant cases occurs during tokenization and creates a lot of redundant cases in Neural Network training.
