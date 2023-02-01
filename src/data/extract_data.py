import json
import os
import numpy as np
import pandas as pd
from tqdm import tqdm
import argparse


parser = argparse.ArgumentParser("Extracting statistical data")
parser.add_argument("--dir",         type=str, default="data/raw/blockdata/normal")
parser.add_argument("--output_path", type=str, default="data/extracted_data/ddos_data.csv")


def extract_statistical_data_from_block(block: dict) -> np.array:
    """
    This function extracts statistical data from a Bitcoin block (block data and transaction data). 
    It takes in a dictionary of the block as an argument and returns an array of the statistical data. 
    The block data includes the number of transactions (n_tx), weight, and size. 
    The transaction data includes the number of inputs and outputs (vin_sz, vout_sz), fee, size, input values (prev_out value), output values, and total value. 
    The function first extracts the individual values for each transaction, then calculates summary statistics for each type of value. 
    These summary statistics include sum, max, min, average, and standard deviation. Finally, it concatenates all of these statistical values into one array and returns it.
    """
    # block data
    n_tx = block["n_tx"]
    weight = block["weight"]
    size = block["size"]

    # transaction data
    all_tx = block["tx"]
    all_n_vin = [ tx["vin_sz"] for tx in all_tx ]
    all_n_vout = [ tx["vout_sz"] for tx in all_tx ]
    all_fee = [ tx["fee"] for tx in all_tx ]
    all_tx_size = [ tx["size"] for tx in all_tx ]
    all_tx_fee = [ tx["fee"] for tx in all_tx ]

    # input, output and value of transaction
    all_vin_value = []
    all_vout_value = []
    all_value = []

    for tx in all_tx:
        tx_vin_value = [ input["prev_out"]["value"]/1e8 for input in tx["inputs"] ]
        tx_vout_value = [ output["value"]/1e8 for output in tx["out"] ]
        tx_value = [ output["value"]/1e8 if output["spent"] == True else -output["value"]/1e8 for output in tx["out"] ]

        all_vin_value.append(tx_vin_value)
        all_vout_value.append(tx_vout_value)
        all_value.append(np.sum(tx_value))

    # Vout_value
    # 1st extraction
    first_all_vout_value = []
    for tx_vout_value in all_vout_value:
        first_all_vout_value.append([np.sum(tx_vout_value), np.max(tx_vout_value), np.min(tx_vout_value), np.average(tx_vout_value), np.std(tx_vout_value)])

    # 2nd extraction
    second_sum_vout_value = np.sum(first_all_vout_value, axis=0)
    second_max_vout_value = np.max(first_all_vout_value, axis=0)
    second_min_vout_value = np.min(first_all_vout_value, axis=0)
    second_avg_vout_value = np.average(first_all_vout_value, axis=0)
    second_std_vout_value = np.std(first_all_vout_value, axis=0)

    # Vin_value
    # 1st extraction
    first_all_vin_value = []
    for tx_vin_value in all_vin_value:
        first_all_vin_value.append([np.sum(tx_vin_value), np.max(tx_vin_value), np.min(tx_vin_value), np.average(tx_vin_value), np.std(tx_vin_value)])

    # 2nd extraction
    second_sum_vin_value = np.sum(first_all_vin_value, axis=0)
    second_max_vin_value = np.max(first_all_vin_value, axis=0)
    second_min_vin_value = np.min(first_all_vin_value, axis=0)
    second_avg_vin_value = np.average(first_all_vin_value, axis=0)
    second_std_vin_value = np.std(first_all_vin_value, axis=0)

    # 2nd extraction of transaction data
    second_n_vin = np.array([np.sum(all_n_vin), np.max(all_n_vin), np.min(all_n_vin), np.average(all_n_vin), np.std(all_n_vin)])
    second_n_vout = np.array([np.sum(all_n_vout), np.max(all_n_vout), np.min(all_n_vout), np.average(all_n_vout), np.std(all_n_vout)])
    second_value = np.array([np.sum(all_value), np.max(all_value), np.min(all_value), np.average(all_value), np.std(all_value)])
    second_tx_fee = np.array([np.sum(all_tx_fee), np.max(all_tx_fee), np.min(all_tx_fee), np.average(all_tx_fee), np.std(all_tx_fee)])
    second_tx_size = np.array([np.sum(all_tx_size), np.max(all_tx_size), np.min(all_tx_size), np.average(all_tx_size), np.std(all_tx_size)])

    # concat all statistical data
    block_data = np.array([n_tx, weight, size])

    statistical_data = np.concatenate([
        block_data,
        second_n_vin, second_n_vout, second_value, second_tx_fee, second_tx_size,
        second_sum_vin_value, second_max_vin_value, second_min_vin_value, second_avg_vin_value, second_std_vin_value,
        second_sum_vout_value, second_max_vout_value, second_min_vout_value, second_avg_vout_value, second_std_vout_value
    ])

    statistical_data = statistical_data.astype(np.float64)

    # assert the dimention of final data
    assert statistical_data.shape == (78,)

    return statistical_data

def extract_statistical_data_from_json(json_path: str) -> np.array:
    """
    This function takes in a JSON file path (json_path) as an argument and returns a NumPy array containing statistical data from the JSON file. 
    It first opens the JSON file and loads the raw data. 
    It then iterates through each block in the raw data, extracting statistical data from each block using the extract_statistical_data_from_block() function. 
    Finally, it concatenates all of the extracted statistical data into a single NumPy array and returns it. 
    """
    with open(json_path) as f:
        raw_data = json.load(f)
    
    all_blocks_statistical_data = []
    for block in raw_data:
        block_statistical_data = extract_statistical_data_from_block(block)
        all_blocks_statistical_data.append(block_statistical_data)
    all_blocks_statistical_data = np.concatenate([all_blocks_statistical_data], axis=1)

    return all_blocks_statistical_data

def extract_statistical_data_from_dir(dir: str, output_path: str) -> None:
    """
    This function takes in two parameters: dir (a string containing the directory path) and output_path (a string containing the output path). 
    It returns a Pandas DataFrame. 
    The function first creates a list of json files from the given directory. 
    It then extracts statistical data from each json file and stores it in a list. 
    The list is then converted to an array. 
    The function then creates column names for the DataFrame, which include nTx, Weight, Size, 
    transaction features with statistical criteria, transaction IO features with two statistical criteria, and Is DDoS Attack ?. 
    The labels are then created based on whether the directory contains "attack" or not.
    The data and labels are combined into an array and used to create the DataFrame. 
    Finally, the DataFrame is saved to the given output path.
    """
    json_files = [file for file in os.listdir(f"{dir}") if file.endswith(".json")]
    all_files_statistical_data = []

    for idx, json_file in tqdm(enumerate(json_files), total=len(json_files)):
        all_blocks_statistical_data = extract_statistical_data_from_json(os.path.join(dir, json_file))
        all_files_statistical_data.extend(all_blocks_statistical_data)
    all_files_statistical_data = np.array(all_files_statistical_data)

    # Create column names 
    df_columns = ["nTx", "Weight", "Size"]

    transaction_features = ["nVin", "nVout", "Value", "Fee", "Tx_Size"]
    transaction_io_features = ["Vout_value", "Vout_value"]
    statistical_criteria = ["Sum", "Max", "Min", "Avg", "Stdv"]

    for transaction_feature in transaction_features:
        for statistical_criterion in statistical_criteria:
            df_columns.append(f"{transaction_feature}_{statistical_criterion}")

    for transaction_feature in transaction_io_features:
        for statistical_criterion_2 in statistical_criteria:
                for statistical_criterion_1 in statistical_criteria:
                        df_columns.append(f"{transaction_feature}_{statistical_criterion_1}_{statistical_criterion_2}")
    
    # Label columns
    df_columns.append("Is DDoS Attack ?")         
    labels = np.array([1] * all_files_statistical_data.shape[0] if "attack" in dir else [0] * all_files_statistical_data.shape[0])
    labels = labels.reshape(-1, 1)
    
    # data and label
    data_and_label = np.concatenate((all_files_statistical_data, labels), axis=1)

    # Create output dir if not exist
    os.makedirs(os.path.split(output_path)[0], exist_ok=True)

    # save the result
    df = pd.DataFrame(data_and_label, columns=df_columns)
    df.to_csv(output_path, index=False)


if __name__ == '__main__':
    args = parser.parse_args()
    extract_statistical_data_from_dir(args.dir, args.output_path)
    