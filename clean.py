import re

stop_chars = ["@", "#", "&", "$"]

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

    for line in pll_org.readlines():
        if line[0] not in stop_chars:
            sumerian_pll.write(pretty_line(line))
            sumerian_pll.write('\n')
        if line.find("#tr.en") != -1:
            english_pll.write(pretty_line(line[7:]))
            english_pll.write('\n')

sumerian_mono()
parallel()