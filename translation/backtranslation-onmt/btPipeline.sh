numShards=9
weightsDir=${1:-../../weights/BT}
shardSrcDir=${2:-./src}
shardBackDir=${3:-./backT}
evalSrcDir=${4:-../../dataset/dataToUse/UrIIICompSents}
evalTgtDir=${5:-./}

for shard in 0 1 2 3 4 5 6 7 8
do
  val=`expr $shard + 1`
  echo $val
  if [ -d "${weightsDir}/${val}st/" ]; then
      echo "found existing, skipping"
  else
    echo "########### Back Translating Sumerian using previous weights ############"
    python3 backtranslateONMT.py --srcFile shard${shard}.sum --model ${weightsDir}/${shard}st/_step_10000.pt
    echo "########### Stacking ############"
    cp ./backed/train.sum ./backed/train${shard}.sum
    cp ./backed/train.eng ./backed/train${shard}.eng
    python3 stack.py --backSrc ${shardSrcDir}/shard${shard}.sum --backTgt ${shardBackDir}/shard${shard}.eng
    mkdir ${weightsDir}/${val}st/
    echo "########### Re-Training ###########"
    sh runTransformerSumEn.sh ../backed ../${weightsDir}/${val}st/
    python3 stack.py --backSrc ${shardSrcDir}/shard${shard}.sum --backTgt ${shardBackDir}/shard${shard}.eng
    mkdir ${weightsDir}/${val}st/
    echo "########### Re-Training ###########"
    sh runTransformerSumEn.sh ./backed ${weightsDir}/${val}st/
    echo "########### Evaluating #############"
    onmt_translate -model ${weightsDir}/${val}st/_step_10000.pt -src ${evalSrcDir}/evaluate.sum -output ${evalTgtDir}/predd_eng${val}.txt -replace_unk -verbose
  fi
done
