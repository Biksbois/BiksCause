import pandas as pd
import sys
from os import path
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

def create_and_add(start, end, duration, csv_name, c_start, c_end, c_duration):
    data = {c_start:[start], c_end:[end],c_duration:[duration]}
    df = pd.DataFrame(data, columns=[c_start, c_end, c_duration])
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
        create_and_add(start, end, duration, csv_name, c_start, c_end, c_duration)

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
    