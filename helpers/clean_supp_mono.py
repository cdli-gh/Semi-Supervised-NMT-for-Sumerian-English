import pandas as pd
import re

stopping_chars=["@", "#", "&", "$"]

df1 = pd.read_csv('../all_sum.csv')

lines = list(df1.values[:, 0])

Original_sumerian_mono = []

def savefile(filename,LIST):
    with open(filename, 'w') as f:
        for line in LIST:
            f.write("%s\n" % line)
            
            
def processing_1(text_line):
    #x = re.sub(r"\[\.+\]","unk",text_line)
    #x = re.sub(r"...","unk",x)
    x = re.sub(r'\#', '', text_line)
    x = re.sub(r"\_", "", x)
    x = re.sub(r"\[", "", x)
    x = re.sub(r"\]", "", x)
    x = re.sub(r"\<", "", x)
    x = re.sub(r"\>", "", x)
    x = re.sub(r"\!", "", x)
    x = re.sub(r"@c", "", x)
    x = re.sub(r"@t", "", x)
    #x=re.sub(r"(x)+","x",x)
    x = re.sub(r"\?", "", x)
    x = x.split()
    x = " ".join(x)
    k = re.search(r"[a-wyzA-Z]+",x)
    if k:
        return x
    else:
        return ""

for j in lines:
    for i in j.split('\n'):
        if len(i)>0 and i[0] not in stopping_chars:
            index=i.find(".")
            l=i[index+1:].strip()
            Original_sumerian_mono.append(l)

print('Data Loaded')

processed_summerian=[] 
for i in range(len(Original_sumerian_mono)):
    text=processing_1(Original_sumerian_mono[i])
    if(re.search("\d\d\d\d\d",text)):
        continue
    if(len(text)>2):
        processed_summerian.append(text)

print('Data Processed')
        
        
savefile('../Dataset/Original_Data/supp_mono.txt', Original_sumerian_mono)
savefile('../Dataset/Cleaned_Data/supp_mono.txt', processed_summerian)

print('Files Saved')