import os
import random

en_path_1 = 'data3/mono/en/all1.en'
en_path_2 = 'data3/mono/en/all2.en'
en_path = 'data3/mono/en/all.en'
sum_path = 'data3/mono/sum/all.sum'

with open(sum_path, 'r') as f:
    sum_lines = f.readlines()

with open(en_path_1, 'r') as f:
    en_lines_1 = f.readlines()

with open(en_path_2, 'r') as f:
    en_lines_2 = f.readlines()

en_lines = en_lines_1
for line in en_lines_2:
    if(len(en_lines) <= len(sum_lines)):
        en_lines.append(line)
    else:
        break

random.shuffle(en_lines)

print(len(en_lines))
print(len(sum_lines))

with open(en_path, 'w') as f:
    f.write(''.join(en_lines))
