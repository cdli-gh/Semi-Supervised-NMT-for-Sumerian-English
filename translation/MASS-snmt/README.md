# MASS (Supervised)

## Install the specific requirements:

```
pip install -r requirements.txt
```

## For Training:

### Data Preperation:

Keep your data files in the following format:

```
- data/
  ├─ mono/
  |  ├─ train.en
  |  ├─ train.sum
  |  ├─ valid.en
  |  ├─ valid.sum
  |  ├─ dict.en.txt
  |  └─ dict.sum.txt
  └─ para/
     ├─ train.en
     ├─ train.sum
     ├─ valid.en
     ├─ valid.sum
     ├─ dict.en.txt
     └─ dict.sum.txt
```
The files under mono are monolingual data, while under para are bilingual data. dict.en(sum).txt in different directory should be identical. The dictionary for different language can be different.

Run the following command to preprocess the data:

```
sh data_prep.sh
```

The processed data will be stored in the ```data/processed``` folder.

### Pre-Training

```
sh pre_training.sh
```

### Fine-Tuning

```
sh fine_tuning.sh
```

Model weights and logs would be stored inside the ```experiments``` folder.


## References

- [MASS with Supervised Pre-training](https://github.com/microsoft/MASS/MASS-supNMT)
