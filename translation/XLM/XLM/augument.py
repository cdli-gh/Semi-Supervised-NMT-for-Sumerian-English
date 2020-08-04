import pandas as pd
import os

with open('./data4/mono/en/all.en', 'r') as f:
	enMono = f.read().split('\n')

enCSV = {'text':enMono, 'labels':[0]*len(enMono)}

pd.DataFrame(enCSV).to_csv('./nonAugumentedEnMono.csv', index=False)

os.system(textattack augment --csv nonAugumentedEnMono.csv --input-column text --pct-words-to-swap 1 --transformations-per-example 3)

enAUG = pd.read_csv('augment.csv')

enAUG = enAUG.sample(frac=1).reset_index(drop=True)

enAUG = list(enAUG['text'])

enAUG1 = []

for line in enAUG:
	if type(line) == str:
		enAUG1.append(line)

print(len(enAUG1))

with open('./data4/mono/en/all.en', 'w') as f:
	f.write('\n'.join(enAUG1))