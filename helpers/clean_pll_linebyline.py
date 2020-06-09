import re

stop_chars = ["@", "#", "&", "$", ">"]

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

def pretty_line_eng(text_line):
    x = re.findall("[ a-zA-Z1-9]+", text_line)
    return ''.join(x)

def parallel():
    pll_org = open("../sumerian_translated.atf", "r")
    sum_org = open("../dataset/original/sumerian_pll.txt", "w")
    eng_org = open("../datastet/original/english_pll.txt", "w")
    sumerian_pll = open("../dataset/cleaned/sumerian_pll.txt", "w")
    english_pll = open("../dataset/cleaned/english_pll.txt", "w")
    lines = pll_org.readlines()
    print(len(lines))
    for i in range(len(lines)):
        if lines[i] != " " and lines[i][0] not in stop_chars:
            index=lines[i].find(".")
            sum_line = pretty_line_sum(lines[i][index+1:])
            while sum_line != "" and sum_line != " ":
                try:
                    i += 1
                    if lines[i].find("#tr.en") != -1:
                        eng_line = pretty_line_eng(lines[i][8:])
                        if eng_line != "" and eng_line != " ":
                            sum_org.write(lines[i][index+1:])
                            eng_org.write(lines[i][8:])
                            sumerian_pll.write(sum_line)
                            english_pll.write(eng_line)
                            sumerian_pll.write('\n')
                            english_pll.write('\n')
                            break
                except:
                    break

parallel()