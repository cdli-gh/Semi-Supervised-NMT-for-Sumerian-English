import pandas as pd
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--saveFile', type='str')

args = parser.parse_args()

with open('pred_engg1.txt') as f:
    preds = f.readlines()

with open('../../dataset/dataToUse/UrIIICompSents/evaluate.sum') as f:
    inps = f.readlines()

with open('../../dataset/dataToUse/UrIIICompSents/evaluate.eng') as f:
    actual = f.readlines()

print(len(preds), len(inps), len(actual))

pd.DataFrame({'input':inps, 'actual':actual, 'preds':preds}).to_csv('./btPreds1.csv')
