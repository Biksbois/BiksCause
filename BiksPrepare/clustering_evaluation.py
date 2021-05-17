import pandas as pd
import numpy as np
import csv
import os
import clustering_method as cm

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

def retrieve_gvf_score(df, cl_col, dur_col):
    gvf = 0
    df_arr = np.asarray(df[dur_col])
    cl_arr = cm.create_cl_arrays(df, dur_col, cl_col)
    if len(cl_arr) > 1:
        print(len(cl_arr))
        gvf = cm.evaluate_gvf(df_arr, cl_arr)
    return gvf

def get_gvf_all_cl(df, cl_arr, dur_col):
    gvf = 0
    for cl_col in cl_arr:
        gvf = retrieve_gvf_score(df, cl_col, dur_col)
    return gvf

def cluster_data_extraction(df, cl_arr, dur_col):
    cluster_dict = {}
    count_clusters = 0
    for index, row in df.iterrows():
        for cl in cl_arr:
            if row[cl] not in cluster_dict:
                cluster_dict[row[cl]] = [row[dur_col], row[dur_col], 1]
            else:
                if check_lower(row[dur_col], cluster_dict[row[cl]][0]):
                    cluster_dict[row[cl]][0] = row[dur_col]
                if check_upper(row[dur_col], cluster_dict[row[cl]][1]):
                    cluster_dict[row[cl]][1] = row[dur_col]
                cluster_dict[row[cl]][2] += 1
    return cluster_dict, get_gvf_all_cl(df, cl_arr, dur_col)

def evaluate_clusters_in_event(df_data_arr, dur_col):
    event_dict = {}
    gvf = 0
    for data in df_data_arr:
        if data[0] not in event_dict:
            event_dict[data[0]] = cluster_data_extraction(data[1], data[2], dur_col)
        else:
            event_dict[data[0]].update(cluster_data_extraction(data[1], data[2], dur_col))
    return event_dict

def convert_dict_to_string(event_dict):
    with open('test.csv', 'w', newline='') as csvfile:
        csv_columns = ['Event','Cluster', 'Interval_Start', 'Interval_End', 'Amount', 'GVF']
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for event, cluster_arr in event_dict.items():
            writer.writerow({'Event': event, 'Cluster': '', 'Interval_Start': '', 'Interval_End': '','Amount': '', 'GVF': ''})
            for cluster, interval in cluster_arr[0].items():
                writer.writerow({'Event': '', 'Cluster': cluster, 'Interval_Start': interval[0], 'Interval_End': interval[1],'Amount': interval[2], 'GVF': ''})
            writer.writerow({'Event': '', 'Cluster': '', 'Interval_Start': '', 'Interval_End': '','Amount': '', 'GVF': cluster_arr[1]})
def create_cluster_files(event_dict, output_path):
    text = open(output_path, 'w')
    clust_text = convert_dict_to_string(event_dict)
    text.close()

def run_evaluation(input_path, output_path = 'temp.txt', dur_col = 'duration', cl_col = 'cluster'):
    csv_paths = scan_directory(input_path)
    df_data_arr = process_csv_files(csv_paths, cl_col)
    event_dict = evaluate_clusters_in_event(df_data_arr, dur_col)
    create_cluster_files(event_dict, output_path)

def evaluate_clust_synthetic(path_1, path_2):
    csv_1, csv_2 = pd.read_csv(path_1), pd.read_csv(path_2)
    mismatch = 0

    for ind in range(len(csv_1)):
        c_1 = csv_1.iloc[[ind]]['events_cluster']
        c_2 = csv_2.iloc[[ind]]['events_cluster']
        if c_1.item() != c_2.item():
            print('Row: {}, Number of mismatches: {}'.format(ind, mismatch))
            mismatch += 1
    
    print('Total amount of rows: {}, amount of mismatches: {}'.format(len(csv_1), mismatch))
        # if csv_1.iloc[[ind]] != csv_2.iloc[[ind]]:
        #     mismatch += 1
        #     print(mismatch)



if __name__ == '__main__':
    path_1 = 'output_csv\generated_data\gen_1.csv'
    path_2 = 'temp.csv'
    evaluate_clust_synthetic(path_1, path_2)