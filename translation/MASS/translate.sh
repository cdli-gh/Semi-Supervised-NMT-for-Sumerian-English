MODEL=$1

fairseq-generate ./data/processed \
	-s sum -t en \
	--user-dir mass \
	--langs en,sum \
	--source-langs sum --target-langs en \
	--mt_steps sum-en \
	--gen-subset valid \
	--task xmasked_seq2seq \
	--path $MODEL \
	--beam 5 \
	--remove-bpe
