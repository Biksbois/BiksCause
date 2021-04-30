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

def add_new_line(temp_csv_path, current_row, i, start, time_colum, c_start, c_end, c_duration, data):
    csv_name = generate_csv_name(temp_csv_path, current_row)
    
    end = i
    duration = delta_time(start, end, data, time_colum)
    
    if path.exists(csv_name):
        add_to_csv(start, end, duration, csv_name, c_start, c_end, c_duration)
    else:
        create_and_add(start, end, duration, csv_name, c_start, c_end, c_duration, current_row)

def extract_start_end(colum, temp_csv_path, i, c_start, c_end, cluster_name):
    csv_path = f"{temp_csv_path}\{colum}.csv"
    csv_file = pd.read_csv(csv_path)
    
    for j in range(len(csv_file[c_start])):
        if i >= int(csv_file[c_start][j]) and i <= int(csv_file[c_end][j]):
            return int(csv_file[c_start][j]), int(csv_file[c_end][j]), csv_file[cluster_name][j]
    print("ERROR")
    return '-ERROR-', '-ERROR-', '-ERROR-'

def count_clusters(c_start, c_end, c_duration, colum, time_colum, temp_csv_path, data):
    start = 0
    end = 0
    duration = 0
    csv_name = ""
    current_row = ''

    empty_folder(temp_csv_path)

    # for i in range(len(data[colum])):
    #     start = i
    #     end = i + 1
    #     current_row = data[colum][i]
    #     add_new_line(temp_csv_path, 'trafic_stuffs', i, start, time_colum, c_start, c_end, c_duration, data)
    
    for i in range(len(data[colum])):
        if current_row != data[colum][i] and current_row != '':
            add_new_line(temp_csv_path, current_row, i, start, time_colum, c_start, c_end, c_duration, data)
            current_row = ''
        
        if current_row == '':
            current_row = data[colum][i]
            start = i
    
    add_new_line(temp_csv_path, current_row, i, start, time_colum, c_start, c_end, c_duration, data)

def create_clusters(c_duration, temp_csv_path, data):
    for file in os.listdir(temp_csv_path):
        temp_path = f"{temp_csv_path}/{file}"
        # print(f"PATH ---------- {temp_path}")
        temp_data = pd.read_csv(temp_path)
        create_cluster(temp_data, temp_path, c_duration, 'cluster', file)

def add_clusters(c_start, c_end, ds_path, colum, cluster_name, new_colum_name, temp_csv_path, data):
    start = 0
    end = 0
    
    new_data = []
    
    for i in range(len(data[colum])):
        if i >= end:
            start, end, cluster = extract_start_end(data[colum][i], temp_csv_path, i, c_start, c_end, cluster_name)
        new_data.append(cluster)

    data[new_colum_name] = new_data
    data.to_csv(ds_path, index=False, header=True)

def generate_clusters(ds_path, colum, time_colum, temp_csv_path, cluster_name = 'cluster'):
    print(f"---\nClusters are about to be generated in file \"{ds_path}\"\n---", flush=True)
    
    data = pd.read_csv(ds_path)
    
    c_start = 'start'
    c_end = 'end'
    c_duration = 'duration'
    new_colum_name = colum + "_cluster"
    
    count_clusters(c_start, c_end, c_duration, colum, time_colum, temp_csv_path, data)
    print("Cluster have successfully been counted.", flush=True)
    create_clusters(c_duration, temp_csv_path, data)
    print("Clusters have successfully been generated.", flush=True)
    add_clusters(c_start, c_end, ds_path, colum, cluster_name, new_colum_name, temp_csv_path, data)
    print("Clusters have successfully been added back into the CSV file.", flush=True)

if __name__ == '__main__':
    from clustering_method import create_cluster
    
    ds_path = u'BiksCalculations\csv\\ny_trafic.csv'
    colum = 'weather_description'
    time_colum = 'date_time'
    temp_csv_path = u'BiksCalculations\csv\\temp_csv'

    generate_clusters(ds_path, colum, time_colum, temp_csv_path)
else:
    from BiksPrepare.clustering_method import create_cluster


