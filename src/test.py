import pandas as pd
import os


metadata_path = "/home/xps/educate/code/hust/Crypto2022/data/raw/metadata"

print(pd.read_csv(f"{metadata_path}/servByDate.csv").iloc[:3])