import pandas as pd
import os
import json
from datetime import datetime
#path
dir = os.environ.get('dir')
block_dir, meta_dir = dir + '/data/raw/blockdata', dir + '/data/raw/metadata'

#convert time to milliseconds
def get_timestamp(file='timestamp.csv'):
    def to_timestamp(time='2013-05-31'):
        y, m, d = [int(i) for i in time.split('-')]
        time = datetime(y, m, d)
        return int(time.timestamp()*1000)
    
    timestamp_df = {'dosday': [], 'postlink': []}
    df = pd.read_csv(f'{meta_dir}/servByDate.csv')
    timestamp_df['dosday'] = df['dosday'].apply(to_timestamp)
    timestamp_df['postlink'] = df['postlink']
    timestamp_df = pd.DataFrame.from_dict(timestamp_df)
    timestamp_df.to_csv(f'{meta_dir}/{file}')

def get_blockhash(file='./test.json'):
    for data in json.load(open(file, 'r')):
        blockhash = data['hash']
        block_api = f"https://blockchain.info/rawblock/{blockhash}"
        os.system(f'curl {block_api} >> {file}')

def get_date(start, end):
    dates = [i.date() for i in pd.date_range(start, end).tolist()]
    timestamps = []
    for i in dates:
        y, m, d = i.year, i.month, i.day
        timestamps.append(int(datetime(y, m, d).timestamp()*1000))
    return timestamps

if __name__ == '__main__':
    # print(get_timestamp()['dosday'][0])
    # timestamp = get_timestamp()['dosday'][0]
    # time_api = f"https://blockchain.info/blocks/{timestamp}?format=json"
    # # block_api = f"https://blockchain.info/rawblock/{block_hash}
    # os.system(f'curl {time_api} > test.json')
    # get_blockhash()
    

    print(get_date(start='2011-02-01', end='2013-10-31'))


