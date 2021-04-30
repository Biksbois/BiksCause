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


def small_trafic_experiment(col_list):
    cause_column, effect_column = get_cause_effect_col()
    ds_path = get_small_traffic()
    result_path = get_result_path()
    experiment_type = get_small_trafic_exp_type()
    ds_obj = init_obj_test_trafic(cause_column=cause_column, effect_column=effect_column, ds_path=ds_path)
    
    run_experiments(ds_obj, cause_column, effect_column, ds_path, result_path, col_list, experiment_type)

def large_trafic_experiment(col_list):
    cause_column, effect_column = get_cause_effect_col()
    ds_path = get_large_traffic()
    result_path = get_result_path()
    experiment_type = get_large_trafic_exp_type()
    ds_obj = init_obj_test_trafic(cause_column=cause_column, effect_column=effect_column, ds_path=ds_path)
    
    run_experiments(ds_obj, cause_column, effect_column, ds_path, result_path, col_list, experiment_type)

def test_cluster():
    pass

def print_not_implemented(message):
    print(f"\n\n---{message}, this feature has not been implemented yet.\n---\n")

def large_test_experiment(cluster_column):
    print_not_implemented('the experiment on a large test dataset')

def small_test_experiment(cluster_column):
    print_not_implemented('the experiment on a small test dataset')

def large_test_cluster(cluster_colum, is_cluster_numbers):
    print_not_implemented('the clustering on a large test dataset')

def small_test_cluster(cluster_colum, is_cluster_numbers):
    print_not_implemented('the clustering on a small test dataset')

def small_trafic_cluster(cluster_colum, is_cluster_numbers):
    ds_path = get_small_traffic()
    time_colum = get_trafic_time()
    temp_csv_path = get_temp_csv_path()

    run_cluster(ds_path, cluster_colum, is_cluster_numbers, time_colum, temp_csv_path)

def large_trafic_cluster(cluster_colum, is_cluster_numbers):
    ds_path = get_large_traffic()
    time_colum = get_trafic_time()
    temp_csv_path = get_temp_csv_path()

    run_cluster(ds_path, cluster_colum, is_cluster_numbers, time_colum, temp_csv_path)


def print_start(is_trafic, is_large, exp_type):
    print(f"---\nThe experiment with the following input will now run:\n  - trafic: {is_trafic}\n  - large: {is_large}\n  - {exp_type}\n")
    

def call_experiment(col_list, is_trafic, is_large):
    if is_trafic:
        if is_large:
            large_trafic_experiment(col_list)
        else:
            small_trafic_experiment(col_list)
    else:
        if is_large:
            large_test_experiment(col_list)
        else:
            small_test_experiment(col_list)

def call_cluster(cluster_colum, is_cluster_numbers, is_trafic, is_large):
    if is_trafic:
        if is_large:
            large_trafic_cluster(cluster_colum, is_cluster_numbers)
        else:
            small_trafic_cluster(cluster_colum, is_cluster_numbers)
    else:
        if is_large:
            large_test_cluster(cluster_colum, is_cluster_numbers)
        else:
            small_test_cluster(cluster_colum, is_cluster_numbers)

if __name__ == '__main__':
    start_time = time.time()
    
    cluster = 'cluster'
    experiment = 'experiment'
    large = 'large'
    small = 'small'
    traffic = 'traffic'
    test = 'test'
    
    is_trafic, is_large, user_input = get_userinput(cluster, experiment, large, traffic, test)
    
    cluster_colum = 'weather_description' ## IMPORTANT! When changing this value, also update 'is_cluster_number'.
    cluster_colum = 'traffic_volume' ## IMPORTANT! When changing this value, also update 'is_cluster_number'.
    is_cluster_numbers = True 
    
    col_list = ['weather_main','weather_description','weather_description_cluster']
    
    if user_input == cluster:
        print_start(is_trafic, is_large, user_input)
        call_cluster(cluster_colum, is_cluster_numbers, is_trafic, is_large)
    elif user_input == experiment:
        print_start(is_trafic, is_large, user_input)
        call_experiment(col_list, is_trafic, is_large)
    elif user_input == '':
        print_start(is_trafic, is_large, f'{cluster} and {experiment}')
        call_cluster(cluster_colum, is_cluster_numbers, is_trafic, is_large)
        call_experiment(col_list, is_trafic, is_large)
    else:
        print("The given input was not valid.\nThe program will now exit.")
    print("\n\n--- %s seconds ---\n\n" % round((time.time() - start_time), 2))