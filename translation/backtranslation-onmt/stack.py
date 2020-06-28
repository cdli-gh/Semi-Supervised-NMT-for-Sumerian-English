import random
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--backSrc', type=str)
parser.add_argument('--backTgt', type=str)

args = parser.parse_args()

pllSrc = './backed/train.sum'
pllTgt = './backed/train.eng'

with open(args.backSrc, 'r') as f:
    bs = f.readlines()

with open(args.backTgt, 'r') as f:
    bt = f.readlines()

with open(pllSrc, 'r') as f:
    pllS = f.readlines()

with open(pllTgt, 'r') as f:
    pllT = f.readlines()

allS = pllS + bs
allT = pllT + bt

all = list(zip(allS, allT))
random.shuffle(all)
allS, allT = zip(*all)

with open(pllSrc, 'w') as f:
    f.write(''.join(allS))

with open(pllTgt, 'w') as f:
    f.write(''.join(allT))
