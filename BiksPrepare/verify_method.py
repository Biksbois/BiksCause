import pandas as pd
import os.path
from os import path
import sys
import csv

def get_headers(name_list, irrelevant_columns):
    ret_list = []
    for name in name_list:
        ret_list.append(irrelevant_columns[name].irrelevant_columns)
    return ret_list

def verify_names_and_columns(name_list, irrelevant_columns, csv_path):
    headers = get_headers(name_list, irrelevant_columns)
    
    if len(name_list) != len(headers):
        sys.exit("An error occurre when checking the length of names and headers.\nPlease check the length of the dictionary and the amount of names defined.")
    
    for i in range(len(headers)):
        file_path = f"{csv_path}/{name_list[i]}.csv"
        if  not path.exists(file_path):
            sys.exit(f"ERROR: The csv path \"{file_path}\" did not exists.")
        
        data = pd.read_csv(file_path)
        cols = data.columns
        
        for h in headers[i]:
            if  not h in cols:
                sys.exit(f"ERROR: the header \"{h}\" is not in \"{file_path}\".\nConsider looking at the list_of_names and the irrelevant_columns.")
