from collections import defaultdict
from tqdm import tqdm
from itertools import combinations
import argparse
import random
import copy

all_label_list = []
lines = []
label_count = defaultdict(int)
co_occurrence = defaultdict(lambda: defaultdict(int))

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--annots",type=str,default="openimages_common_214_ram_annots.txt")
    parser.add_argument("--sample_num",type=int,default=10)
    parser.add_argument("--result_path",type=str,default="result.txt")
    parser.add_argument("--prompt",type=str,default="Is there a {} in the image?")
    parser.add_argument("--sample_method",type=str,default="random")

    args = parser.parse_args()

    return args


def preprocess(annots:str)->None:
    global all_label_list
    with open(annots,'r') as f:
        for line in tqdm(f):
            img_path = line.strip().split(',')[0]
            labels = line.strip().split(',')[1:]
            lines.append( (img_path,labels) )

            for label1, label2 in combinations(labels,2):
                co_occurrence[label1][label2] += 1
                co_occurrence[label2][label1] += 1

            for label in labels:
                label_count[label] += 1

    all_label_list = list(label_count.keys())
    all_label_list.sort(key=lambda x: label_count[x], reverse=True)

    # Sort the co_occurrence dict
    for key, value in co_occurrence.items():
        co_occurrence[key] = sorted(value.items(), key=lambda x: x[1], reverse=True)



def create_question(img:str,label:str,template:str,expected_answer:str):
    return {
        "img": img,
        "question": template.format(label),
        "expected_answer": expected_answer
    }



def POPE(template:str, method:str, sample_num:int) -> list():
    result = []
    for img_path,labels in tqdm(lines):
        history_object_list = copy.deepcopy(labels)

        # Generate positive sample
        ground_truth = [create_question(img_path,label,template,'yes') for label in labels]
        result.extend(ground_truth)

        # Negative sampling (random)
        for _ in range(len(ground_truth)):
            if method == "random":
                selected_object = random.choice(all_label_list)
                while selected_object in history_object_list:
                    selected_object = random.choice(all_label_list)
                result.append(create_question(img_path,selected_object,template,'no'))
                history_object_list.append(selected_object)
            
            # Negative sampling(popular)
            elif method == "popular":
                for selected_label in all_label_list:
                    if selected_label in history_object_list: continue
                    result.append(create_question(img_path,selected_label,template,'no'))
                    history_object_list.append(selected_label)
                    break       
            
            # Negative sampling(adversarial)
            elif method == "adversarial":
                flag = 0
                
                target_object = random.choice(labels)
                for selected_object,_ in co_occurrence[target_object]:
                    if selected_object not in history_object_list:
                        result.append(create_question(img_path,selected_object,template,'no'))
                        history_object_list.append(selected_object)
                        flag = 1
                        break

                #In case flag=0 -> random choice
                if not flag:
                    selected_object = random.choice(all_label_list)
                    while selected_object in history_object_list:
                        selected_object = random.choice(all_label_list)
                    result.append(create_question(img_path,selected_object,template,'no'))
                    history_object_list.append(selected_object)

    return result


def finishprocess(result:list, result_path:str)->None:
    with open(result_path,'w') as f:
        for item in result:
            line = '\t'.join([item['img'], item['question'], item['expected_answer']])
            f.write(line + '\n')


def main():
    config = parse_args()
    preprocess(config.annots)
    result = POPE(config.prompt,config.sample_method,config.sample_num)
    finishprocess(result,config.result_path)



if __name__ == "__main__":
    main()