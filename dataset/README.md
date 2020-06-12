# Dataset Description

All of the data in this folder has been derived from the raw files present in the main folder, namely ```../all_sum.csv```, ```../sumerian_untranslated.atf```,  ```../all_sum_parallel.csv``` and ```../sumerian_translated.atf```, where the first two files contain the monolingual Sumerian data and the later two contain parallel data for Sumerian-English.

A sample complete sentence from the raw data is as follows:

```
&P011012 = WF 055 
#atf: lang sux 
@tablet 
@obverse 
@column 1 
1. 1(u@c) 1(asz@c) 2(barig@c) sze gur-mah 
#tr.en: 11 gurmaḫ 2 barig barley,
2. ganun-mah 
#tr.en: from Big-Storehouse; 
3. 6(asz@c) sze gur 
#tr.en: 6 gur(maḫ) barley, 
4. 3(asz@c) 1/2(asz@c) 2(barig@c) ganun 
#tr.en: 3 1/2 (gurmaḫ) 2 barig, storehouse,
```

As can be seen, we have line by line translated sentences. Concatenating all the lines of a language would give us a complete sentence corresponding to that language.

Thus, we have divided our parallel data into 4 broad categories:
- UrIII Admin Data with complete sentence translations
- UrIII Admin Data with line by line translations
- All kinds of Sumerian Data with complete sentence translations
- All kinds of Sumerian Dtaa with line by line translations

While, we would be using the same test data for evaluation, which corresponds to UrIII Admin Data with complete sentences.

## Files and Folders

```original```: Contains data extracted from the raw files without any additional preprocessing <br>
```cleaned```: Contains cleaned data for each of the 4 categories <br>
```dataToUse```: Contains cleaned data divided into training, testing and validation sets <br>
