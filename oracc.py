import argparse
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument('--inputfile', '-i', help="Input ATF file", required=True)
parser.add_argument('--output', '-o', help="Output file name", required=True)
args = parser.parse_args()

inp = args.inputfile
out = args.output

with open(inp, 'r') as f:
    data = f.readlines()

id=None

id_list = []
lang_list = []
sumerian_list = []
english_list = []

for i in range(len(data)):
    if data[i].startswith('&'):
        id = data[i].split(" ")[0].strip('&')
    elif data[i].startswith("#atf: "):
        lang = data[i].split('lang')[-1].strip()
    elif data[i].startswith('@'):
        continue
    elif data[i][0].isdigit():
        lang_list.append(lang)
        id_list.append(id)
        sumerian_list.append(data[i].strip('\n'))
        if data[i+1].startswith("#tr.en: "):
            a = data[i+1].strip('#tr.en: ')
            if a!='\n':
                english_list.append(a.strip('\n'))
            else:
                english_list.append('N/A')
            i+=1
        else:
            english_list.append("N/A")
    else:
        continue



df = pd.DataFrame({'ID':id_list, 'lang':lang_list, 'sumerian_unclean':sumerian_list, 'english_unclean':english_list})
df.to_csv(out+'.csv', index=False)
