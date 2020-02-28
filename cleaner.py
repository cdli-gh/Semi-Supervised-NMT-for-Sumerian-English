import argparse
import pandas as pd
import re

def sumerian_cleaner(df):
    data = df['sumerian_unclean']
    punctuations = '-?<>/$%&@#*+=^\{\}.:;|`~'
    regex = re.compile('[%s]' % re.escape(punctuations))
    ## Flag corresponding damaged sentences
    if '[' in data and ']' in data:
        return "---DAMAGED STRING---"

    else:

        data = data.split(" ")
        for i in range(len(data)):
            data[i] = re.sub('[0-9]', '', data[i])  #Removes all the place value numbers
            data[i] = data[i].replace('(disz)', 'NUMB')   #Replaces (disz) as NUMB
            if data[i].startswith('_'): #Converts _lugal_ to LUGAL as stated in the points. This may not be necessary as in normalizing the data, it will again be converted to lower case
                data[i] = data[i].replace('_', '')
                data[i] = data[i].upper()
            data[i] = regex.sub('', data[i])    #Removes all unnecessary punctuations other than ! and ()
            if data[i].endswith('!'):
                data[i] = data[i].replace('!', '')    #If there are no corrections
            elif '!' in data[i] and '(' in data[i]:
                temp = re.search('\((.*)\)', data[i])
                data[i] = temp.group(1).lower()     #Discard the other string and use the corrected string


        return ' '.join(data).lower().strip(" ").replace('(','').replace(")","")


parser = argparse.ArgumentParser()
parser.add_argument("--input", '-i', help="input csv file", required=True)
args = parser.parse_args()

inp = args.input

data = pd.read_csv(inp.strip('.csv')+'.csv')
data['cleaned_sumerian'] = data.apply(sumerian_cleaner, axis=1)



data.to_csv("sumerian_cleaned.csv", index=False)
