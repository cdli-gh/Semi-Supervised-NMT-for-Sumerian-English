import pandas as pd
import re

stop_chars=["@", "&", "$", "#", ">"]

with open('../dataset/dataToUse/UrIIICompSents/test.sum', 'r') as f:
    test = f.read().split('\n')

with open('../dataset/dataToUse/allCompSents/train.sum', 'r') as f:
    train = f.read().split('\n')

df1 = pd.read_csv('../all_sum.csv')

lines = list(df1.values[:, 0])
      
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

def pretty_line_sum(text_line):
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

def parallel(lines_r):
    # pll_org = open("../sumerian_translated.atf", "r")
    sum_org = open("../dataset/original/supp_sum_mono3.txt", "w")
    # eng_org = open("../dataset/original/supp_eng_pll2.txt", "w")
    sumerian_pll = open("../dataset/cleaned/allCompSents/mono.sum", "w")
    # english_pll = open("../dataset/cleaned/allCompSents/pll.eng", "a")
    # lines = pll_org.readlines()
    # print(len(lines_r))
    for lines in lines_r:
        if(lines.find('#atf: lang sux') == -1):
            continue
        try:
            lines = lines.split('\n')
        except:
            continue
        # print(len(lines))
        sum_lines = []
        # eng_lines = []
        org_sum_lines = []
        # org_eng_lines = []
        count_words = 0
        for i in range(len(lines)):
            if lines[i] != "" and lines[i] != " " and lines[i][0] not in stop_chars:
                index=lines[i].find(".")
                sum_line = pretty_line_sum(lines[i][index+1:])
                count_words += len(sum_line.split())
                if(sum_line not in sum_lines):
                    sum_lines.append(sum_line)
                    org_sum_lines.append(lines[i][index+1:])

            if count_words>5 or len(sum_lines) >= 3 or i == len(lines)-1 and count_words:
                sum_org.write(' '.join(org_sum_lines))
                # eng_org.write(' '.join(org_eng_lines))
                if(' '.join(sum_lines) not in test and ' '.join(sum_lines) not in train):
                    sumerian_pll.write(' '.join(sum_lines))
                # english_pll.write(' '.join(eng_lines))
                    sumerian_pll.write('\n')
                # english_pll.write('\n')
                sum_lines = []
                # eng_lines = []
                org_sum_lines = []
                # org_eng_lines = []
                count_words = 0
                    
parallel(lines)