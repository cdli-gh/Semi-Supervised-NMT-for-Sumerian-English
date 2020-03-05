import re

# the code references pr #6
def clean_sumerian(line):
    punctuations = '-?<>/$%&@#*+=^\{\}.:;|`~_!\(\)\[\]'
    regex = re.compile('[%s]' % re.escape(punctuations))
    items = line.split(" ")
    for i in range(len(items)):
        items[i] = items[i].lower()
        items[i] = re.sub('[0-9]', '', items[i])
        items[i] = items[i].replace('(disz)', 'NUMB')
        if '!' in items[i] and '(' in items[i] and ')' in items[i]:
            temp = re.search('\((.*)\)', items[i])
            items[i] = temp.group(1).lower()
        items[i] = regex.sub('', items[i])

    return ' '.join(items).strip()

def clean_translated(path):
    with open(path, 'r') as f:
        lines = f.readlines()
    i = 0
    lan_pairs = []
    while i < len(lines) - 1:
        line = lines[i].strip()
        next_line = lines[i+1].strip()
        i += 1
        if not line:
            continue
        if line[0].isdigit() and next_line.startswith('#tr.en'):
            l1 = ' '.join(line.split(' ')[1:])
            l1 = clean_sumerian(l1)
            l2 = next_line.replace('#tr.en: ', '')
            if l1:
                lan_pairs.append((l1, l2))
            i += 1
    lan_pairs = list(set(lan_pairs))
    return lan_pairs

def clean_untranslated(path):
    with open(path, 'r') as f:
        lines = f.readlines()
    i = 0
    lan = []
    while i < len(lines):
        line = lines[i].strip()
        i += 1
        if not line:
            continue
        if line[0].isdigit():
            l1 = ' '.join(line.split(' ')[1:])
            l1 = clean_sumerian(l1)
            if l1:
                lan.append(l1)
            i += 1
    lan = list(set(lan))
    return lan

def list2file(path, lst):
    with open(path, 'w', encoding='utf-8') as f:
        for l in lst:
            f.write(l + '\n')

if __name__ == "__main__":
    translated_path = 'sumerian_translated.atf'
    untranslated_path = 'sumerian_untranslated.atf'
    lan_pairs = clean_translated(translated_path)
    su = [p[0] for p in lan_pairs]
    en = [p[1] for p in lan_pairs]
    list2file('sumerian_translated_cleaned.txt', su)
    list2file('english_translated_cleaned.txt', en)
    lan = clean_untranslated(untranslated_path)
    list2file('sumerian_untranslated_cleaned.txt', lan)