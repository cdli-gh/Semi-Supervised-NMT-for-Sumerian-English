import re

stop_chars = ["@", "#", "&", "$", ">"]

def pretty_line(text_line):
    x = re.sub(r'\([^)]*\)', ' ', text_line)
    x = re.sub("[1-9]+", " NUMB", x[2:])
    x = re.findall("[a-zA-Z]+", x)
    x = re.sub(r'\b(\w+)( \1\b)+', r'\1', ' '.join(x))
    return x

def sumerian_mono():
    mono_org = open("../sumerian_untranslated.atf", "r")
    sumerian_mono = open("../Dataset/New_Data/sumerian_mono.atf", "w")

    for line in mono_org.readlines():
        if line != " " and line[0] not in stop_chars:
            line = pretty_line(line)
            if line != "" and line != " ":
                sumerian_mono.write(line)
                sumerian_mono.write('\n')

sumerian_mono()