import pandas as pd
import os
import json
from pprint import pprint
path = "/home/tranbaochi_/Study/hust/Crypto2022/data/raw/blockdata/attack/attack_0_5.json"
# for i in range(5):
#     os.environ['a'] = str(int(os.environ['a']) + 1)
#     print(os.environ['a'])
# def test_func():
#     a = 3
#     b = 4
#     def test():
#         a = int(os.environ['a'])
#         a += 1
#         os.environ['a'] = str(a)

#     test()
#     return os.environ['a']

path1 = "/home/tranbaochi_/Study/hust/Crypto2022/data/raw/blockdata/attack/attack_0_5.json"
path2 = "/home/tranbaochi_/Study/hust/Crypto2022/data/raw/blockdata/attack/attack_5_50.json"

for file in json.load(open(path1, 'r')):
    for file_ in json.load(open(path2, 'r')):
        if file == file_:
            print(file)