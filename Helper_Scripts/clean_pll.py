import re

stop_chars = ["@", "#", "&", "$", ">"]

def pretty_line_sum(text_line):
    x = re.sub(r'\([^)]*\)', ' ', text_line)
    x = re.sub("[1-9]+", " NUMB", x[2:])
    x = re.findall("[a-zA-Z]+", x)
    x = re.sub(r'\b(\w+)( \1\b)+', r'\1', ' '.join(x))
    return x

def pretty_line_eng(text_line):
    x = re.findall("[a-zA-Z1-9 ]+", text_line)
    return ''.join(x)

def parallel():
    pll_org = open("../sumerian_translated.atf", "r")
    sumerian_pll = open("../Dataset/New_Data/sumerian_pll.atf", "w")
    english_pll = open("../Dataset/New_Data/english_pll.atf", "w")
    lines = pll_org.readlines()
    print(len(lines))
    for i in range(len(lines)):
        if lines[i] != " " and lines[i][0] not in stop_chars:
            sum_line = pretty_line_sum(lines[i])
            while sum_line != "" and sum_line != " ":
                try:
                    i += 1
                    if lines[i].find("#tr.en") != -1:
                        eng_line = pretty_line_eng(lines[i][8:])
                        if eng_line != "" and eng_line != " ":
                            sumerian_pll.write(sum_line)
                            english_pll.write(eng_line)
                            sumerian_pll.write('\n')
                            english_pll.write('\n')
                            break
                except:
                    break

parallel()