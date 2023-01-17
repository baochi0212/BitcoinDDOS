import pandas as pd
import os
import json
from pprint import pprint
path = "/home/tranbaochi_/Study/hust/Crypto2022/data/raw/metadata/attack.json"
for i in range(5):
    os.environ['a'] = str(int(os.environ['a']) + 1)
    print(os.environ['a'])
# def test_func():
#     a = 3
#     b = 4
#     def test():
#         a = int(os.environ['a'])
#         a += 1
#         os.environ['a'] = str(a)

#     test()
#     return os.environ['a']

# print(test_func())
pprint(len(json.load(open(path, 'r'))))