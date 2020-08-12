import os
import argparse

parser = argparse.ArgumentParser()

parser.add_argument('--srcFile', type=str)
parser.add_argument('--savedir', type=str, default='./backT')
parser.add_argument('--model', type=str, default='../../weights/BT/1st/weights_step_13000.pt')

args = parser.parse_args()

# saveName = 'shard' + str(int(args.model.split('/')[-2][-3])) + '.eng'
saveName = 'shard' + str(int(args.model.split('/')[-2][-3])+1) + '.eng'

print(args.srcFile)
if(saveName not in os.listdir(args.savedir)):
    os.system(f'onmt_translate -model {args.model} -src src/{args.srcFile} -output {args.savedir}/{saveName} -replace_unk -verbose')
else:
    print('Already Exists')
