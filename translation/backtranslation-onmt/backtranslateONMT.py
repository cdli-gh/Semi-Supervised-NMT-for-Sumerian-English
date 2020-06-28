import os
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--savedir', type=str, default='./backT')
parser.add_argument('--model', type=str, default='../../weights/BT/1st/weights_step_13000.pt')

args = parser.parse_args()

saveName = 'shard' + args.model.split('/')[-2][-3] + '.eng'

for file in os.listdir('./src'):
  print(file)
  if(saveName not in os.listdir(savedir)):
      os.system(f'onmt_translate -model {args.model} -src src/{file} -output {args.savedir}/{saveName} -replace_unk -verbose')
      break
