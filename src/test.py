import pandas as pd
import os
import json
path = "/home/tranbaochi_/Study/hust/Crypto2022/src/data/test.json"
os.environ['a'] = "3"
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
print(json.load(open("/home/tranbaochi_/Study/hust/Crypto2022/data/raw/blockdata/normal.json", 'r'))[0].keys())
