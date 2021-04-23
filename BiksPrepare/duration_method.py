import pandas as pd
import sys
from os import path
from clustering_method import create_cluster

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
        csv_writer.writerow([start, end, duration, csv_name])

def create_and_add(start, end, duration, csv_name, c_start, c_end, c_duration, cluster_col):
    data = {c_start:[start], c_end:[end],c_duration:[duration], cluster_col:[csv_name]}
    df = pd.DataFrame(data, columns=[c_start, c_end, c_duration, cluster_col])
    df.to_csv(csv_name, index=False, header=True)

def translate_date(date):
    return datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S') # 2012-10-02 09:00:00

def calc_deltatime(t1, t2):
    diff = t2-t1
    days, seconds = diff.days, diff.seconds
    hours = days * 24 + seconds // 3600
    return hours

def delta_time(start, end, data, time_colum):
    return calc_deltatime(translate_date(data[time_colum][start]), translate_date((data[time_colum][end])))

def add_new_line(temp_csv_path, current_row, i, start, time_colum, c_start, c_end, c_duration):
    csv_name = generate_csv_name(temp_csv_path, current_row)
    
    end = i
    duration = delta_time(start, end, data, time_colum)
    
    if path.exists(csv_name):
        add_to_csv(start, end, duration, csv_name, c_start, c_end, c_duration)
    else:
        create_and_add(start, end, duration, csv_name, c_start, c_end, c_duration, current_row)

def extract_start_end(colum, temp_csv_path, i, c_start, c_end):
    csv_path = f"{temp_csv_path}/{colum}.csv"
    csv_file = pd.read_csv(csv_path)
    
    for j in range(len(csv_file[c_start])):
        if i >= int(csv_file[c_start][j]):
            return int(csv_file[c_start][j]), int(csv_file[c_end][j]), csv_file[colum][j]
    print("ERROR")
    return '', '', ''

if __name__ == '__main__':
    ds_path = u'BiksCalculations\csv\\ny_trafic.csv'
    data = pd.read_csv(ds_path)
    colum = 'weather_description'
    time_colum = 'date_time'
    new_colum_name = colum + "_cluster"
    current_row = ''
    temp_csv_path = u'BiksCalculations\csv\\temp_csv'
    c_start = 'start'
    c_end = 'end'
    c_duration = 'duration'
    
    start = 0
    end = 0
    duration = 0
    csv_name = ""
    
    empty_folder(temp_csv_path)
    
    for i in range(len(data[colum])):
        if current_row != data[colum][i] and current_row != '':
            add_new_line(temp_csv_path, current_row, i, start, time_colum, c_start, c_end, c_duration)
            
            current_row = ''
        
        if current_row == '':
            current_row = data[colum][i]
            start = i
    
    add_new_line(temp_csv_path, current_row, i, start, time_colum, c_start, c_end, c_duration)
    
    # for file in os.listdir(temp_csv_path):
    #     temp_path = f"{temp_csv_path}/{file}"
    #     temp_data = pd.read_csv(temp_path)
    #     create_cluster(temp_data, temp_path, c_duration)
    
    start = 0
    end = 0
    
    new_data = []
    
    for i in range(len(data[colum])):
        if i <= start or i >= end:
            start, end, cluster = extract_start_end(data[colum][i], temp_csv_path, i, c_start, c_end)
        new_data.append(cluster)
    data[new_colum_name] = new_data
    data.to_csv(ds_path, index=False, header=True)
    