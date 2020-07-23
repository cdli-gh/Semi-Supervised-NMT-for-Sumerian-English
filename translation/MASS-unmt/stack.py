import random
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--src', type=str)
parser.add_argument('--tgt', type=str)

args = parser.parse_args()

all = []
for file in os.listdir(f'XLM/{args.src}'):
    try:
        with open(args.backSrc, 'r') as f:
            all += f.readlines()
    except:
        continue

random.shuffle(all)

with open(f'XLM/{args.tgt}', 'w') as f:
    f.write(''.join(allS))
