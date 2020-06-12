import os
import numpy as np

types = ["train", "test", "dev"]

savedir = '../dataset/dataToUse/allCompSents/'
urdir = '../dataset/dataToUse/UrIIICompSents/'

def savefile(filename,LIST):
    with open(savedir + filename, 'a') as f:
        for line in LIST:
            f.write("%s" % line)

for filee in os.listdir(urdir):
    for t in types:
        lines_s = ""
        lines_e = ""
        if(filee[:filee.find('.')] == t):
            with open(urdir + filee, 'r') as f:
                if filee[-3:] == 'sum':
                    lines_s += f.read()
                elif filee[-3:] == 'eng':
                    lines_e += f.read()
            
            savefile(t + '.sum', lines_s)
            savefile(t + '.eng', lines_e)

with open('../dataset/dataToUse/UrIIICompSents/test.sum', 'r') as f:
    test_sents = f.read()

test_sents = test_sents.split('\n')

with open('../dataset/dataToUse/allCompSents/train.sum', 'r') as f:
    train_sents = f.read()

with open('../dataset/dataToUse/allCompSents/train.eng', 'r') as f:
    train_sents2 = f.read()

train_sents = train_sents.split('\n')
train_sents2 = train_sents2.split('\n')

print(len(train_sents), len(train_sents2))

for i in range(len(train_sents)):
    while(train_sents[i].find('Q') != -1):
        idx = train_sents[i].find('Q')
        train_sents[i] = train_sents[i][0:idx] + train_sents[i][idx+12:]

for i in range(len(train_sents)):
    try:
        if train_sents[i] in test_sents or len(train_sents2[i]) == 0 or train_sents2[i] == '':
            train_sents.pop(i)
            train_sents2.pop(i)
            i-=1
    except:
        break

print(len(train_sents), len(train_sents2))

with open('../dataset/dataToUse/allCompSents/trainX.eng', 'w') as f:
    f.write('\n'.join(train_sents2))

with open('../dataset/dataToUse/allCompSents/trainX.sum', 'w') as f:
    f.write('\n'.join(train_sents))