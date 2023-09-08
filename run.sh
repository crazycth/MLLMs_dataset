python process.py --sample_method=random --result_path=output/random.txt
python process.py --sample_method=adversarial --result_path=output/adversarial.txt
python process.py --sample_method=popular --result_path=output/popular.txt

echo random采样数据量: `wc -l output/random.txt | awk '{print $1}'` 
echo adversarial采样数据量: `wc -l output/adversarial.txt | awk '{print $1}'`
echo popular采样数据量: `wc -l output/popular.txt | awk '{print $1}'`