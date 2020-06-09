import os
import numpy as np

types = ["train", "test", "dev"]

savedir = '../dataset/dataToUse/allCompSents/'
urdir = '../dataset/dataToUse/UrIIICompSents/'

def savefile(filename,LIST):
    with open(savedir + filename, 'a') as f:
        for line in LIST:
            f.write("%s" % line)

for filee in os.listdir(urdir):
    for t in types:
        lines_s = ""
        lines_e = ""
        if(filee[:filee.find('.')] == t):
            with open(urdir + filee, 'r') as f:
                if filee[-3:] == 'sum':
                    lines_s += f.read()
                elif filee[-3:] == 'eng':
                    lines_e += f.read()
            
            savefile(t + '.sum', lines_s)
            savefile(t + '.eng', lines_e)