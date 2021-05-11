import sys
import itertools
import time
import pandas as pd
from experiment_obj import exp_obj
from BiksPrepare.duration_method import generate_clusters
from BiksCalculations.calc_main import do_calculations
from BiksCalculations.dataset_object import init_obj_test_trafic
from main_paths import *
from BiksCalculations.find_potential_parents import *

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

def run_experiments(ds_obj, cause_column, effect_column, ds_path, result_path, cluster_col, baseline_col, e_obj, window_size, use_optimizer=True, hardcoded_cir_m=None):
    for w in window_size:
        e_obj.window_size = w
        ds_obj.window_size = w
        
        if not hardcoded_cir_m == None and w in hardcoded_cir_m:
            print("SET AS STUFF")
            ds_obj.hardcoded_cir_m = hardcoded_cir_m[w]
        else:
            ds_obj.hardcoded_cir_m = None
        
        print(f"---\nThe experiments with clusters will now run for window size {w}\n---", flush=True)
        
<<<<<<< HEAD
        do_calculations(ds_obj, cause_column, effect_column, result_path + "\\cluster", cluster_col, ds_path, e_obj, use_optimizer=use_optimizer)

        print(f"---\nThe experiments without clusters will now run for window size {w}\n---", flush=True)

=======
        #do_calculations(ds_obj, cause_column, effect_column, result_path + "\\cluster", cluster_col, ds_path, e_obj, use_optimizer=use_optimizer)
>>>>>>> 4031b7552df70049f2a347ffa4c56990e7d05143
        do_calculations(ds_obj, cause_column, effect_column, result_path + "\\no_cluster", baseline_col, ds_path, e_obj, use_optimizer=use_optimizer)
    
    print("\nThe experiments are now successfully done, and the program will exit.")

# def small_trafic_experiment(cluster_col, baseline_col, e_obj, window_size, use_optimizer=True):
#     cause_column, effect_column = get_cause_effect_col()
#     result_path = get_result_path()
    
#     ds_path = get_small_traffic()
#     experiment_type = get_small_trafic_exp_type()
#     ds_obj = init_obj_test_trafic(cause_column=cause_column, effect_column=effect_column, ds_path=ds_path, windows_size=e_obj.window_size, head_val=e_obj.head_val)
    
#     run_experiments(ds_obj, cause_column, effect_column, ds_path, result_path, cluster_col, baseline_col, e_obj, window_size, use_optimizer=True)

# def large_trafic_experiment(colcluster_col, baseline_col_list, e_obj, window_size):
#     cause_column, effect_column = get_cause_effect_col()
#     result_path = get_result_path()
    
#     ds_path = get_large_traffic()
#     # experiment_type = get_large_trafic_exp_type()
#     ds_obj = init_obj_test_trafic(cause_column=cause_column, effect_column=effect_column, ds_path=ds_path, windows_size=e_obj.window_size, head_val=e_obj.head_val)
    
#     run_experiments(ds_obj, cause_column, effect_column, ds_path, result_path, cluster_col, baseline_col, e_obj, window_size)

def call_experiment(trafic_cluster_col, trafic_baseline_col, medical_cluster_col, medical_baseline_col, is_trafic, is_large, e_obj, window_size, hardcoded_cir_m):
    cause_column, effect_column = get_cause_effect_col()
    result_path = get_result_path()

    if is_trafic:
        ds_path = get_large_traffic()
        cluster_col = trafic_cluster_col
        baseline_col = trafic_baseline_col
        time_colum = 'date_time'
        ds_obj = init_obj_test_trafic(cause_column=cause_column, effect_column=effect_column, ds_path=ds_path, windows_size=e_obj.window_size, head_val=e_obj.head_val)
    else:
        ds_path = get_large_medical()
        cluster_col = medical_cluster_col
        baseline_col = medical_baseline_col
        time_colum = ('start', 'stop')
        ds_obj = None #TODO: Make this one
    
    run_experiments(ds_obj, cause_column, effect_column, ds_path, result_path, cluster_col, baseline_col, e_obj, window_size, hardcoded_cir_m=hardcoded_cir_m)

def test_cluster():
    pass

def print_not_implemented(message):
    print(f"\n\n---{message}, this feature has not been implemented yet.\n---\n")

def large_medical_experiment(cluster_col, baseline_col, e_obj, window_size):
    pass

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

def print_start(is_trafic, is_large, exp_type, window_size, head_val_small, head_val_large, lambda_val, alpha_val, support, scores):
    if is_large:
        message = head_val_large
    else:
        message = head_val_small
    
    print(f"---\nThe experiment with the following input will now run:\n  - trafic: {is_trafic}\n  - large: {is_large}\n  - {exp_type}\n  - windowsize: {window_size}\n  - head_val = {message}\n  - alpha values: {alpha_val}\n  - lambda values: {lambda_val}\n  - support: {support}\n  - scores: {scores}")

def print_scores(scores, window_size, head_val):
    print(head_val)

def call_cluster(trafic_cluster_colums, medical_cluster_columns, is_trafic, is_large):
    if is_trafic:
        if is_large:
            large_trafic_cluster(trafic_cluster_colums)
        else:
            small_trafic_cluster(trafic_cluster_colums)
    else:
        if is_large:
            large_test_cluster(medical_cluster_columns)
        else:
            small_test_cluster(medical_cluster_columns)

def init_exp_obj(is_large, is_trafic, traffic, test, large, small, alpha_val, lambda_val, window_size, small_head_val, large_head_val, support, scores):
    if is_large:
        exp_size = large
        head_val = large_head_val
    else:
        exp_size = small
        head_val = small_head_val
    if is_trafic:
        exp_type = traffic
    else:
        exp_type = test
    
    return exp_obj(alpha_val, lambda_val, window_size, head_val, exp_type, exp_size, support, scores)

if __name__ == '__main__':
    start_time = time.time()
    
    cluster = 'cluster'
    experiment = 'experiment'
    large = 'large'
    small = 'small'
    traffic = 'traffic'
    test = 'medical'
    
    head_val_small = 1000
    head_val_large = 50000
    
<<<<<<< HEAD
    window_size = [1] #, 5, 10]
    # window_size = [6, 12, 18, 24]
    alpha_val = [0.55, 0.66, 0.77]
    lambda_val = [0.4, 0.5, 0.7]
=======
    window_size = [1, 3, 6, 12, 18, 24]
    alpha_val = [0.0,0.33,0.44,0.55, 0.66, 0.77,1,2,3,4,5]
    lambda_val = [0.2, 0.3, 0.4, 0.5, 0.7]
>>>>>>> 4031b7552df70049f2a347ffa4c56990e7d05143
    
    scores = ['cir_c', 'cir_b', 'cir_m_avg', 'cir_m_max', 'cir_m_min'] # More keys are added in the constructor
    # scores.extend(e_obj.nst_keys)
    
    support = 10
    
    is_trafic, is_large, user_input = get_userinput(cluster, experiment, large, traffic, test)
    e_obj = init_exp_obj(is_large, is_trafic, traffic, test, large, small, 
                        alpha_val, lambda_val, -1, head_val_small, head_val_large, support, scores)
    
    trafic_cluster_colums = [('traffic_volume', True), ('temp', True), ('clouds_all', True), ('weather_description', False)]
    medical_cluster_columns = []
    
    trafic_column_list = ['temp_cluster','traffic_volume_cluster']
    
    trafic_cluster_col = ['weather_description_cluster'] + trafic_column_list
    trafic_baseline_col = ['weather_description'] + trafic_column_list
    
    medical_column_list = ['deathdate','prefix','marital','race','ethnicity','gender','birthplace']
    
    medical_cluster_col = [] + medical_column_list
    medical_baseline_col = [] + medical_column_list
    
    hardcoded_cir_m = {
        1:{
            'traffic_volume_0': ['heavy intensity rain_0', 'mist_0', 'moderate rain_0', 'traffic_volume_0', 'traffic_volume_2'],
            'traffic_volume_1': ['mist_0', 'moderate rain_0', 'traffic_volume_1', 'light rain_0'],
            'traffic_volume_2': ['moderate rain_0', 'light rain_0', 'heavy intensity rain_0', 'traffic_volume_1', 'traffic_volume_2']
        },
        5:{
            'traffic_volume_0': ['mist_0', 'traffic_volume_0', 'traffic_volume_1', 'traffic_volume_2'],
            'traffic_volume_1': ['mist_0', 'traffic_volume_0', 'traffic_volume_1', 'traffic_volume_2'],
            'traffic_volume_2': ['mist_0', 'traffic_volume_0', 'traffic_volume_1', 'traffic_volume_2'],
        },
        10:{
            'traffic_volume_0': ['moderate rain_0', 'snow_0', 'traffic_volume_0', 'traffic_volume_1'],
            'traffic_volume_1': ['mist_0', 'traffic_volume_0', 'traffic_volume_1', 'traffic_volume_2'],
            'traffic_volume_2': ['mist_0', 'traffic_volume_0', 'traffic_volume_1', 'traffic_volume_2'],
        }}
    
    if user_input == cluster or user_input == '':
        call_cluster(trafic_cluster_colums, medical_cluster_columns, is_trafic, is_large)
    elif user_input == experiment or user_input == '':
        print_start(is_trafic, is_large, user_input, window_size, head_val_small, head_val_large, lambda_val, alpha_val, support, e_obj.scores)
        # e_obj = init_exp_obj(is_large, is_trafic, traffic, test, large, small, alpha_val, lambda_val, window_size, head_val_small, head_val_large, support)
        call_experiment(trafic_cluster_col, trafic_baseline_col, medical_cluster_col, medical_baseline_col, is_trafic, is_large, e_obj, window_size, hardcoded_cir_m)
        print_scores(scores, window_size, head_val_large if is_large else head_val_small)
    else:
        print("The given input was not valid.\nThe program will now exit.")
    
    print("\n\n--- %s seconds ---\n\n" % round((time.time() - start_time), 2))
    