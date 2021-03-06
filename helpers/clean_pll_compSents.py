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
    eng_org = open("../dataset/original/english_pll.txt", "w")
    sumerian_pll = open("../dataset/cleaned/allCompSents/pll.sum", "w")
    english_pll = open("../dataset/cleaned/allCompSents/pll.eng", "w")
    lines_r = pll_org.read()
    # print(len(lines))
    for lines in lines_r.split('1. '):
        lines = lines.split('\n')
        # print(len(lines))
        sum_lines = []
        eng_lines = []
        org_sum_lines = []
        org_eng_lines = []
        count_words = 0
        for i in range(len(lines)):
            if lines[i] != "" and lines[i] != " " and lines[i][0] not in stop_chars:
                index=lines[i].find(".")
                sum_line = pretty_line_sum(lines[i][index+1:])
                if(sum_line not in sum_lines):
                    sum_lines.append(sum_line)
                    org_sum_lines.append(lines[i][index+1:])
                while sum_line != "" and sum_line != " ":
                    try:
                        i += 1
                        if lines[i].find("#tr.en") != -1:
                            eng_line = pretty_line_eng(lines[i][8:])
                            org_eng_lines.append(lines[i][8:])
                            if eng_line != "" and eng_line != " ":
                                eng_lines.append(eng_line)
                                break
                    except:
                        break

            if count_words>5 or len(sum_lines) >= 3 or i == len(lines)-1 and count_words and ' '.join(org_eng_lines) != '\n':
                sum_org.write(' '.join(org_sum_lines))
                eng_org.write(' '.join(org_eng_lines))
                sumerian_pll.write(' '.join(sum_lines))
                english_pll.write(' '.join(eng_lines))
                sumerian_pll.write('\n')
                english_pll.write('\n')
                sum_lines = []
                eng_lines = []
                org_sum_lines = []
                org_eng_lines = []
                count_words = 0
 
parallel()