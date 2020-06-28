numShards=9
for shard in 0 1 2 3 4 5 6 7 8
do
  val=`expr $shard + 1`
  if [ -f ../../weights/BT/${val}st ]; then
      echo "found existing, skipping"
  else
    echo "############################ Back Translating Sumerian using previous weights ############################"
    python3 backtranslateONMT.py --model ../../weights/BT/${shard}st/weights_step_10000.pt
    echo "############################ Stacking ############################"
    python3 stack.py --backSrc ./src/shard${shard}.sum ./backT/shard${shard}.eng
    mkdir ../../weights/BT/${val}st/
    echo "############################ Re-Training ############################"
    sh runTransformerSumEn.sh ./backed ../../weights/BT/${val}st/
    echo "############################ Evaluating ############################"
    onmt_translate -model ../../weights/BT/${val}st/weights_step_10000.pt -src ../../../dataset/dataToUse/UrIIICompSents/evaluate.sum -output ./predd_eng${val}.txt -replace_unk -verbose
  fi
done
