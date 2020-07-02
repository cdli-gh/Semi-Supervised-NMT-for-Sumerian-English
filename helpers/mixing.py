import os
import numpy as np

# types = ["train", "test", "dev"]

# savedir = '../dataset/dataToUse/allCompSents/'
# urdir = '../dataset/dataToUse/UrIIICompSents/'

# def savefile(filename,LIST):
#     with open(savedir + filename, 'a') as f:
#         for line in LIST:
#             f.write("%s" % line)

# for filee in os.listdir(urdir):
#     for t in types:
#         lines_s = ""
#         lines_e = ""
#         if(filee[:filee.find('.')] == t):
#             with open(urdir + filee, 'r') as f:
#                 if filee[-3:] == 'sum':
#                     lines_s += f.read()
#                 elif filee[-3:] == 'eng':
#                     lines_e += f.read()
            
#             savefile(t + '.sum', lines_s)
#             savefile(t + '.eng', lines_e)

with open('../dataset/dataToUse/UrIIICompSents/test.sum', 'r') as f:
    test_sents = f.read()

with open('../dataset/dataToUse/UrIIICompSents/dev.sum', 'r') as f:
    dev_sents = f.read()

with open('../dataset/dataToUse/UrIIICompSents/test.eng', 'r') as f:
    test_sentsPll = f.read()

with open('../dataset/dataToUse/UrIIICompSents/dev.eng', 'r') as f:
    dev_sentsPll = f.read()

test_sents = test_sents.split('\n')
test_sents += dev_sents.split('\n')

test_sentsPll = test_sentsPll.split('\n')
test_sentsPll += dev_sentsPll.split('\n')

with open('../dataset/dataToUse/allCompSents/train.sum', 'r') as f:
    train_sents = f.read()

with open('../dataset/dataToUse/allCompSents/train.eng', 'r') as f:
    train_sents2 = f.read()

train_sents = train_sents.split('\n')
train_sents2 = train_sents2.split('\n')

print(len(train_sents), len(train_sents2))
print(len(test_sents), len(test_sentsPll))

toKeep = []
toKeepPll = []

for i in range(len(test_sents)):
    if(len(test_sents[i].split()) >= 4 and test_sentsPll[i].find('xxx') == -1 and len(test_sentsPll[i].split()) >= 4):
        toKeep.append(test_sents[i])
        toKeepPll.append(test_sentsPll[i])

for i in range(len(train_sents)):
    while(train_sents[i].find('Q') != -1):
        idx = train_sents[i].find('Q')
        train_sents[i] = train_sents[i][0:idx] + train_sents[i][idx+12:]

print(len(toKeep), len(toKeepPll))

with open('../dataset/dataToUse/UrIIICompSents/evaluate.sum', 'w') as f:
    f.write('\n'.join(toKeep))

with open('../dataset/dataToUse/UrIIICompSents/evaluate.eng', 'w') as f:
    f.write('\n'.join(toKeepPll))

# for i in range(len(train_sents)):
#     try:
#         if train_sents[i] in test_sents or len(train_sents2[i]) == 0 or train_sents2[i] == '':
#             train_sents.pop(i)
#             train_sents2.pop(i)
#             i-=1
#     except:
#         break

# print(len(train_sents), len(train_sents2))

# with open('../dataset/dataToUse/allCompSents/trainX.eng', 'w') as f:
#     f.write('\n'.join(train_sents2))

# with open('../dataset/dataToUse/allCompSents/trainX.sum', 'w') as f:
#     f.write('\n'.join(train_sents))