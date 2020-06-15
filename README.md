![](https://nelc.ucla.edu/wp-content/uploads/2019/05/Screen-Shot-2019-05-15-at-4.12.48-PM.png)


# Sumerian-English Unsupervised Neural Machine Translation
As part of the MTAAC project, the organization hosts Sumerian data comprising 1.5 million transliteration lines and 10K parallel lines corpus (approx). We already developed a neural network-based encode-decoder architecture for English-Sumerian Machine Translation, but that leverages the parallel dataset only, which is not sufficient to achieve state-of-the-art results. The task is to develop a language model using the monolingual data as well as parallel data to translate Sumerian phrases to English, and vice-versa.

## Mentors:
1. Niko Schenk
2. Ravneet Punia

## Tasks:

- [x] Preparing the parallel and monolingual texts for final usage. Using methods like BPE and BBPE to tokenize the text.
- [x] Implementing the Vanilla Transformer for Sumerian to English as well as English to Sumerian
- [ ] Back Translating Sumerian Monolingual Text
- [ ] XLM Encoder along with a Transformer Decoder on English-Sumerian Translation.
- [ ] Model-Level Dual Learning using tied Transformer Encoder-Decoder pairs.
