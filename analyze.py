from collections import defaultdict
from tqdm import tqdm

def count_labels(file_path):
    label_count = defaultdict(int)
    with open(file_path, 'r') as f:
        for line in tqdm(f):
            labels = line.strip().split(',')[1:]
            for label in labels:
                label_count[label] += 1
    return label_count

file_path = 'openimages_common_214_ram_annots.txt'  # 请将此处替换为您的txt文件路径
label_count = count_labels(file_path)

if __name__ == "__main__":
    print(f"总共有 {len(label_count)} 类标签。")
    for label, count in label_count.items():
        print(f"标签 '{label}' 出现了 {count} 次。")
