import re
import json

def build_index(pages_content):
    index = {}
    for url, text in pages_content.items():
        # 提取单词，转小写 [cite: 19]
        words = re.findall(r'\w+', text.lower())
        for pos, word in enumerate(words):
            if word not in index:
                index[word] = {}
            if url not in index[word]:
                index[word][url] = []
            index[word][url].append(pos) # 存储位置 [cite: 18]
    return index

def save_index(index, filename="data/index.json"):
    with open(filename, 'w') as f:
        json.dump(index, f)

def load_index(filename="data/index.json"):
    with open(filename, 'r') as f:
        return json.load(f)