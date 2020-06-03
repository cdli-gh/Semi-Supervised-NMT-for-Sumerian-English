import numpy as np
import os

split_ratio = 0.2

def savefile(filename,LIST):
    with open(filename, 'w') as f:
        for line in LIST:
            f.write("%s" % line)

files = os.listdir('../Dataset/Cleaned_Data/')
for fil in files:
    
    with open('../Dataset/Cleaned_Data/english_pll.txt', 'r') as f:
        lines_e = f.readlines()

    with open('../Dataset/Cleaned_Data/sumerian_pll.txt', 'r') as f:
        lines_s = f.readlines()

chosen = []
test_e = []
test_s = []

for i in range(int(len(lines_e)*split_ratio)):
    num = np.random.randint(0, len(lines_s)-1)
    if(num in chosen):
        i-=1
        continue
    chosen.append(num)
    test_e.append(lines_e[num])
    test_s.append(lines_s[num])
    lines_e.pop(num)
    lines_s.pop(num)

savefile('../Dataset/Data_to_use/sum_test.txt', test_s)
savefile('../Dataset/Data_to_use/eng_test.txt', test_e)
savefile('../Dataset/Data_to_use/sum_train.txt', lines_s)
savefile('../Dataset/Data_to_use/eng_train.txt', lines_e)

print('Files Saved')