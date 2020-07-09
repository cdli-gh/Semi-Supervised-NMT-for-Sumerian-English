![](https://nelc.ucla.edu/wp-content/uploads/2019/05/Screen-Shot-2019-05-15-at-4.12.48-PM.png)


# Sumerian-English Unsupervised Neural Machine Translation
As a part of the MTAAC project at CDLI, we aim to build an end-to-end NMT Pipeline while making use of the extensive monolingual Sumerian Data. 

Previous models that have been used to carry out English<-->Sumerian Translation have only made use of the available parallel corpora. Presently we have only about 50K extracted sentences for both languages in the parallel corpora, whereas around 1.47M sentences in the Sumerian monolingual corpus. 

This huge amount of monolingual data can be used to improve the NMT system by combining it with techniques like Back Translation, Tranfer Learning and Dual Learning which have proved specially useful for Low-Resource languages like Sumerian which have a limited amount of parallel data. Moreover, we also look to implement models like XLM and MASS for the same.


## Requirements
Python 3.5.2 or higher <br>
NumPy <br>
Pandas <br>
PyTorch <br>
Torch Text <br>
OpenNMT-py <br>
fairseq <br>


## Repository Structure

<details><summary><b>dataset</b></summary>
  <p>
    Contains the datasets used for training and validating Sumerian<->English NMT. 
     <details><summary><b>dataToUse</b></summary>
          <p>
            Contains all the parallel data divided among traing, test and dev sets, in the 4 different categories:
            - UrIIICompSents <br>
            - AllCompSents <br>
            - UrIIILineByLine <br>
            - AllLineByLIne <br>
          </p>
    </details>
     <details><summary><b>cleaned</b></summary>
          <p>
            Contains data after cleaning using the helper scripts, contains the monolingual data as well:
            - UrIIICompSents <br>
            - AllCompSents <br>
            - UrIIILineByLine <br>
            - AllLineByLIne <br>
          </p>
    </details>
    <details><summary><b>orginal</b></summary>
      <p> Contains all of the data before cleaning </br>
    </details>
    <details><summary><b>oldFormat</b></summary>
      <p> Contains data from last year, for comparison </br>
    </details>
  </p>
</details>
    
<details><summary><b>translation</b></summary>
  <p>
    <details><summary><b>transformer</b></summary>
          <p>
            Contains implemntation of the Vanilla Transformer using parallel data, for Sumerian-English
          </p>
    </details>
     <details><summary><b>backtranslation</b></summary>
          <p>
            Makes use of fairseq to carry out Sumerian-English Back Translation using Sumerian monolingual data
          </p>
    </details>
    <details><summary><b>backtranslation-onmt</b></summary>
          <p>
            Makes use of fairseq and OpenNMT to carry out Sumerian-English Back Translation using Sumerian monolingual data
          </p>
    </details>
</details>

(Refer to the README of each folder and sub-folder to know them in more detail)

## Results

TO DO

For reproducing the results, refer the documentation in the sub-folders inside ```translation```.

## Mentors:
1. Niko Schenk
2. Ravneet Punia

## Tasks:

- [x] Preparing the parallel and monolingual texts for final usage. Using methods like BPE and BBPE to tokenize the text.
- [x] Implementing the Vanilla Transformer for Sumerian to English as well as English to Sumerian
- [x] Back Translation using Sumerian Monolingual data
- [ ] XLM Encoder along with a Transformer Decoder on English-Sumerian Translation.
- [ ] Model-Level Dual Learning using tied Transformer Encoder-Decoder pairs.
