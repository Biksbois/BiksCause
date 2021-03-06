import pandas as pd
import sys
from os import path
from tqdm import trange
from BiksCalculations.time_conversion import *

import datetime
from csv import writer
import os, shutil

def empty_folder(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

def generate_csv_name(csv_path, current_row):
    return f"{csv_path}\{current_row}.csv"

def add_to_csv(start, end, duration, csv_name, c_start, c_end, c_duration):
    with open(csv_name, 'a+', newline='') as write_obj:
        csv_writer = writer(write_obj)
        csv_writer.writerow([start, end, duration])

def create_and_add(start, end, duration, csv_name, c_start, c_end, c_duration, cluster_col):
    data = {c_start:[start], c_end:[end],c_duration:[duration]}
    df = pd.DataFrame(data, columns=[c_start, c_end, c_duration])
    df.to_csv(csv_name, index=False, header=True)

def delta_time(start, end, data, time_colum):
    return calc_deltatime(translate_date(data[time_colum][start]), translate_date((data[time_colum][end])))

def add_new_line(temp_csv_path, current_row, i, start, time_colum, c_start, c_end, c_duration, data, is_cluster_numbers, colum):
    csv_name = generate_csv_name(temp_csv_path, current_row)
    
    end = i
    
    if is_cluster_numbers:
        duration = data[colum][i]
    else:
        duration = delta_time(start, end, data, time_colum)
    
    if path.exists(csv_name):
        add_to_csv(start, end, duration, csv_name, c_start, c_end, c_duration)
    else:
        create_and_add(start, end, duration, csv_name, c_start, c_end, c_duration, current_row)

def extract_start_end(colum, temp_csv_path, i, c_start, c_end, cluster_name, j_end, is_cluster_numbers):
    csv_path = f"{temp_csv_path}\{colum}.csv"
    csv_file = pd.read_csv(csv_path)
    
    start = j_end if is_cluster_numbers else 0
    # start = 0
    
    for j in range(start, len(csv_file[c_start])):
        if i >= int(csv_file[c_start][j]) and i <= int(csv_file[c_end][j]):
            cluster_name = str(csv_file[cluster_name][j]).replace('.csv', '')
            return int(csv_file[c_start][j]), int(csv_file[c_end][j]), cluster_name, j - 1 if j - 1 > 0 and is_cluster_numbers else 0
    
    print(f"c_start = {c_start}\npath = {csv_path}\ni={i}\nj={j}")
    print("\n\n--- ERROR in 'extract_start_end' ---\n\n")
    return '-ERROR-', '-ERROR-', '-ERROR-', '-ERROR-'

def count_clusters(c_start, c_end, c_duration, colum, time_colum, temp_csv_path, data, is_cluster_numbers, csv_if_number):
    start = 0
    end = 0
    duration = 0
    csv_name = ""
    current_row = ''
    
    empty_folder(temp_csv_path)
    
    if is_cluster_numbers:
        for i in trange(len(data[colum])):
            start = i
            end = i + 1
            current_row = data[colum][i]
            add_new_line(temp_csv_path, csv_if_number, i, start, time_colum, c_start, c_end, c_duration, data, is_cluster_numbers, colum)
        add_new_line(temp_csv_path, csv_if_number, i, start, time_colum, c_start, c_end, c_duration, data, is_cluster_numbers, colum)
    else:
        for i in trange(len(data[colum])):
            if current_row != data[colum][i] and current_row != '':
                add_new_line(temp_csv_path, current_row, i, start, time_colum, c_start, c_end, c_duration, data, is_cluster_numbers, colum)
                current_row = ''
            
            if current_row == '':
                current_row = data[colum][i]
                start = i
        add_new_line(temp_csv_path, current_row, i, start, time_colum, c_start, c_end, c_duration, data, is_cluster_numbers, colum)

def create_clusters(c_duration, temp_csv_path, data):
    
    for f in trange(len(os.listdir(temp_csv_path))):
        file = os.listdir(temp_csv_path)[f]
        temp_path = f"{temp_csv_path}/{file}"
        temp_data = pd.read_csv(temp_path)
        create_cluster(temp_data, temp_path, c_duration, 'cluster', file.replace('.csv', ''))

def add_clusters(c_start, c_end, ds_path, colum, cluster_name, new_colum_name, temp_csv_path, data, is_cluster_numbers, csv_if_number):
    start = 0
    end = 0
    
    new_data = []
    j_end = 0
    for i in trange(len(data[colum])):
        if i >= end:
            csv_to_test = csv_if_number if is_cluster_numbers else data[colum][i] 
            start, end, cluster, j_end = extract_start_end(csv_to_test, temp_csv_path, i, c_start, c_end, cluster_name, j_end, is_cluster_numbers)
        new_data.append(cluster)

    data[new_colum_name] = new_data
    data.to_csv(ds_path, index=False, header=True)

def ensure_col_exists(colum, data, ds_path):
    if not colum in data:
        print(f"\n\n---\nERROR: The csv: '{ds_path}'\nDid not contain the column {colum} (duration_method.generate_clusters)")
        exit()

def generate_clusters(ds_path, colum, is_cluster_numbers, time_colum, temp_csv_path, cluster_name = 'cluster'):
    print(f"---\nClusters are about to be generated in file \"{ds_path}\"\n---", flush=True)
    
    data = pd.read_csv(ds_path)
    
    c_start = 'start'
    c_end = 'end'
    c_duration = 'duration'
    new_colum_name = colum + "_cluster"
    
    csv_if_number = colum
    
    ensure_col_exists(colum, data, ds_path)
    ensure_col_exists(time_colum, data, ds_path)
    
    count_clusters(c_start, c_end, c_duration, colum, time_colum, temp_csv_path, data, is_cluster_numbers, csv_if_number)
    print("Step 1/3 - Cluster have successfully been counted.", flush=True)
    create_clusters(c_duration, temp_csv_path, data)
    print("Step 2/3 - Clusters have successfully been generated.", flush=True)
    add_clusters(c_start, c_end, ds_path, colum, cluster_name, new_colum_name, temp_csv_path, data, is_cluster_numbers, csv_if_number)
    print("Step 3/3 - Clusters have successfully been added back into the CSV file.", flush=True)

if __name__ == '__main__':
    from clustering_method import create_cluster
    
    ds_path = u'BiksCalculations\csv\\ny_trafic.csv'
    colum = 'weather_description'
    time_colum = 'date_time'
    temp_csv_path = u'BiksCalculations\csv\\temp_csv'

    generate_clusters(ds_path, colum, time_colum, temp_csv_path)
else:
    from BiksPrepare.clustering_method import create_cluster


