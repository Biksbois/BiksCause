import pandas as pd
import os



def scan_directory(path):
    csv_paths = []
    for file in os.listdir(path):
        if file.endswith(".csv"):
            csv_paths.append(os.path.join(path, file))
    return csv_paths  

def extract_cluster_column(df, cl_name):
    cl_name_arr = []
    for col in df.columns:
        if cl_name in col:
            cl_name_arr.append(col)
    return cl_name_arr

def process_csv_files(csv_paths, cl_col):
    cl_name_arr, df_data_arr = [], []
    for path in csv_paths:
        event_name = path.split('.')[0].split('\\')[-1]
        df = pd.read_csv(path)
        cl_name_arr = extract_cluster_column(df, cl_col)
        df_data_arr.append((event_name, df, cl_name_arr))
    return df_data_arr          

def check_lower(duration, cur_lower):
    return duration < cur_lower

def check_upper(duration, cur_upper):
    return duration > cur_upper

def add_upper_lower_cl_arr(cl_arr):
    new_cl_arr = []
    lower_upper = [0, 0]
    for cl in cl_arr:
        new_cl_arr.append((cl, lower_upper))
    return new_cl_arr

def iniate_check(ul_bound, dur):
    if cl[1][0] == 0:
        cl[1][0] = row[dur_col]
    if cl[1][1] == 0:
        cl[1][1] = row[dur_col]
    if check_lower(row[dur_col], cl[1][0]):
        cl[1][0] = row[dur_col]
    if check_upper(row[dur_col], cl[1][1]):
        cl[1][1] = row[dur_col]


def find_cluster_durations(df, cl_arr, dur_col):
    cl_ul_arr = add_upper_lower_cl_arr(cl_arr)
    event_arr = {}
    for index, row in df.iterrows():
        for cl in cl_arr:
            print(row[cl[0]])
            # if row[cl[0]] not in event_dict:
            #     event_dict[row[cl[0]]] = [0, 0]
            # else:
            #     if check_lower(row[dur_col], event_dict[cl[0]][0]):
            #         event_dict[cl[0]][0] = row[dur_col]
            #     if check_upper(row[dur_col], event_dict[cl[0]][1]):
            #         event_dict[cl[0]][1] = row[dur_col]

def evaluate_clusters_in_event(df_data_arr, dur_col):
    for data in df_data_arr:
        find_cluster_durations(data[1], data[2], dur_col)
        #find_cluster_durations(df, dur_col, cl_arr)

def create_cluster_files():
    pass

def run_evaluation(path, dur_col = 'duration', cl_col = 'cluster'):
    csv_paths = scan_directory(path)
    df_data_arr = process_csv_files(csv_paths, cl_col)
    event_arr = evaluate_clusters_in_event(df_data_arr, dur_col)

if __name__ == '__main__':
    run_evaluation(r'BiksCalculations\csv\temp_csv')