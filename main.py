import sys
import time

from BiksPrepare.duration_method import generate_clusters
from BiksCalculations.calc_main import do_calculations
from BiksCalculations.dataset_object import init_obj_test_trafic
from main_paths import *

def get_userinput(cluster, experiment, large, traffic, test):
    if len(sys.argv) >= 2:
        is_large = large in str(sys.argv[1:])
        is_trafic = not test in str(sys.argv[1:])
        
        if cluster in str(sys.argv[1:]) and experiment in str(sys.argv[1:]) or not cluster in str(sys.argv[1:]) and not experiment in str(sys.argv[1:]):
            return is_trafic, is_large, ''
        elif cluster in str(sys.argv[1:]):
            return is_trafic, is_large, cluster
        elif experiment in str(sys.argv[1:]):
            return is_trafic, is_large, experiment
        else:
            return True, True, 'ERROR'
    else:
        return True, False, ''

def run_cluster(ds_path, cluster_colum, is_cluster_numbers, time_colum, temp_csv_path):
    generate_clusters(ds_path, cluster_colum, is_cluster_numbers, time_colum, temp_csv_path)

def run_experiments(ds_obj, cause_column, effect_column, ds_path, result_path, col_list, experiment_type, use_optimizer=True):
    do_calculations(ds_obj, cause_column, effect_column, result_path, col_list, experiment_type, ds_path, use_optimizer=use_optimizer)
    print("The experiments are now successfully done, and the program will exit.")


def small_trafic_experiment(col_list, window_size):
    cause_column, effect_column = get_cause_effect_col()
    result_path = get_result_path()
    
    ds_path = get_small_traffic()
    experiment_type = get_small_trafic_exp_type()
    ds_obj = init_obj_test_trafic(cause_column=cause_column, effect_column=effect_column, ds_path=ds_path, windows_size=window_size)
    
    run_experiments(ds_obj, cause_column, effect_column, ds_path, result_path, col_list, experiment_type)

def large_trafic_experiment(col_list, window_size):
    cause_column, effect_column = get_cause_effect_col()
    result_path = get_result_path()
    
    ds_path = get_large_traffic()
    experiment_type = get_large_trafic_exp_type()
    ds_obj = init_obj_test_trafic(cause_column=cause_column, effect_column=effect_column, ds_path=ds_path, windows_size=window_size)
    
    run_experiments(ds_obj, cause_column, effect_column, ds_path, result_path, col_list, experiment_type)

def test_cluster():
    pass

def print_not_implemented(message):
    print(f"\n\n---{message}, this feature has not been implemented yet.\n---\n")

def large_test_experiment(cluster_column):
    print_not_implemented('the experiment on a large test dataset')

def small_test_experiment(cluster_column):
    print_not_implemented('the experiment on a small test dataset')

def large_test_cluster(cluster_colums):
    print_not_implemented('the clustering on a large test dataset')

def small_test_cluster(cluster_colums):
    print_not_implemented('the clustering on a small test dataset')

def small_trafic_cluster(cluster_colums):
    ds_path = get_small_traffic()
    time_colum = get_trafic_time()
    temp_csv_path = get_temp_csv_path()

    for c in cluster_colums:
        is_number = c[1]
        col_name = c[0]
        
        run_cluster(ds_path, col_name, is_number, time_colum, temp_csv_path)

def large_trafic_cluster(cluster_colums):
    ds_path = get_large_traffic()
    time_colum = get_trafic_time()
    temp_csv_path = get_temp_csv_path()

    for c in cluster_colums:
        is_number = c[1]
        col_name = c[0]
        
        run_cluster(ds_path, col_name, is_number, time_colum, temp_csv_path)


def print_start(is_trafic, is_large, exp_type, window_size):
    print(f"---\nThe experiment with the following input will now run:\n  - trafic: {is_trafic}\n  - large: {is_large}\n  - {exp_type}\n  - windowsize: {window_size}")
    

def call_experiment(col_list, is_trafic, is_large, window_size):
    if is_trafic:
        if is_large:
            large_trafic_experiment(col_list, window_size)
        else:
            small_trafic_experiment(col_list, window_size)
    else:
        if is_large:
            large_test_experiment(col_list)
        else:
            small_test_experiment(col_list)

def call_cluster(cluster_colums, is_trafic, is_large):
    if is_trafic:
        if is_large:
            large_trafic_cluster(cluster_colums)
        else:
            small_trafic_cluster(cluster_colums)
    else:
        if is_large:
            large_test_cluster(cluster_colums)
        else:
            small_test_cluster(cluster_colums)

if __name__ == '__main__':
    start_time = time.time()
    
    cluster = 'cluster'
    experiment = 'experiment'
    large = 'large'
    small = 'small'
    traffic = 'traffic'
    test = 'test'
    
    window_size = 3
    
    is_trafic, is_large, user_input = get_userinput(cluster, experiment, large, traffic, test)
    
    cluster_colums = [('traffic_volume', True), ('weather_description', False)]
    
    col_list = ['weather_description_cluster', 'traffic_volume_cluster']
    
    if user_input == cluster:
        print_start(is_trafic, is_large, user_input, window_size)
        call_cluster(cluster_colums, is_trafic, is_large)
    elif user_input == experiment:
        print_start(is_trafic, is_large, user_input, window_size)
        call_experiment(col_list, is_trafic, is_large, window_size)
    elif user_input == '':
        print_start(is_trafic, is_large, f'{cluster} and {experiment}', window_size)
        call_cluster(cluster_colums, is_trafic, is_large)
        call_experiment(col_list, is_trafic, is_large, window_size)
    else:
        print("The given input was not valid.\nThe program will now exit.")
    
    print("\n\n--- %s seconds ---\n\n" % round((time.time() - start_time), 2))