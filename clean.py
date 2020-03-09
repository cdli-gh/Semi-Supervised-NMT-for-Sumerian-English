import re

stop_chars = ["@", "#", "&", "$", ">"]

def pretty_line(text_line):
    x = re.findall("[a-zA-Z ]", text_line)
    return ''.join(x[1:])

def sumerian_mono():
    mono_org = open("sumerian_untranslated.atf", "r")
    sumerian_mono = open("sumerian_mono.atf", "w")

    for line in mono_org.readlines():
        if line != " " and line[0] not in stop_chars:
            sumerian_mono.write(pretty_line(line))
            sumerian_mono.write('\n')

def parallel():
    pll_org = open("sumerian_translated.atf", "r")
    sumerian_pll = open("sumerian_pll.atf", "w")
    english_pll = open("english_pll.atf", "w")
    lines = pll_org.readlines()
    print(len(lines))
    for i in range(len(lines)):
        if lines[i] != " " and lines[i][0] not in stop_chars:
            sumerian_pll.write(pretty_line(lines[i]))
            sumerian_pll.write('\n')
            while True:
                try:
                    i += 1
                    if lines[i].find("#tr.en") != -1:
                        english_pll.write(pretty_line(lines[i][7:]))
                        english_pll.write('\n')
                        break
                except:
                    break

sumerian_mono()
parallel()
