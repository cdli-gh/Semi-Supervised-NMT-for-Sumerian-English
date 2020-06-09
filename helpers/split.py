import numpy as np
import os

split_ratio = 0.2

subfolder = 'allLineByLine/'
datadir = '../dataset/cleaned/'+subfolder
savedir = '../dataset/dataToUse/'+subfolder

def savefile(filename,LIST):
    with open(savedir + filename, 'w') as f:
        for line in LIST:
            f.write("%s" % line)

with open(datadir + 'pll.eng', 'r') as f:
    lines_e = f.readlines()

with open(datadir + 'pll.sum', 'r') as f:
    lines_s = f.readlines()

chosen = []
test_e = []
test_s = []
train_e = []
train_s = []

for i in range(int(len(lines_e)*(1-split_ratio))):
    num = np.random.randint(0, len(lines_s)-1)
    if(num in chosen or 'xxx' in lines_e[num].split() or lines_e == ''):
        i-=1
        continue
    chosen.append(num)
    train_e.append(lines_e[num])
    train_s.append(lines_s[num])

for i in range(int(len(lines_e)*split_ratio)):
    num = np.random.randint(0, len(lines_s)-1)
    if(num in chosen or lines_s[num] in train_s):
        i-=1
        continue
    chosen.append(num)
    test_e.append(lines_e[num])
    test_s.append(lines_s[num])

dev_e = []
dev_s = []

for i in range(int(len(lines_e)*split_ratio/2)):
    num = np.random.randint(0, len(lines_s)-1)
    if(num in chosen or lines_s[num] in train_s):
        i-=1
        continue
    chosen.append(num)
    dev_e.append(lines_e[num])
    dev_s.append(lines_s[num])

savefile('test.sum', test_s)
savefile('test.eng', test_e)
savefile('dev.sum', dev_s)
savefile('dev.eng', dev_e)
savefile('train.sum', train_s)
savefile('train.eng', train_e)

print('Files Saved')