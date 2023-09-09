#!/bin/bash

python process.py --sample_method=random --result_path=output/random.txt "$@"
python process.py --sample_method=adversarial --result_path=output/adversarial.txt "$@"
python process.py --sample_method=popular --result_path=output/popular.txt "$@"

rm tem.txt

echo random QA num: `wc -l output/random.txt | awk '{print $1}'` 
echo adversarial QA num: `wc -l output/adversarial.txt | awk '{print $1}'`
echo popular QA num: `wc -l output/popular.txt | awk '{print $1}'`