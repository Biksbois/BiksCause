import sys
import time

from BiksPrepare.duration_method import generate_clusters
from BiksCalculations.calc_main import do_calculations
from BiksCalculations.dataset_object import init_obj_test_trafic
from main_paths import *

def get_userinput():
    if len(sys.argv) >= 2:
        return str(sys.argv[1])
    else:
        return ''

def run_cluster(cluster_colum):
    generate_clusters(ds_path, cluster_colum, time_colum, temp_csv_path)

def run_experiments(cause_column, effect_column, ds_path, result_path, col_list, experiment_type, use_optimizer=True):
    ds_obj = init_obj_test_trafic(cause_column=cause_column, effect_column=effect_column, ds_path=ds_path)

    do_calculations(ds_obj, cause_column, effect_column, result_path, col_list, experiment_type, ds_path, use_optimizer=use_optimizer)
    print("The experiments are now successfully done, and the program will exit.")


def small_trafic_experiment(col_list):
    cause_column, effect_column = get_cause_effect_col()
    ds_path = get_small_traffic()
    result_path = get_result_path()
    experiment_type = get_small_trafic_exp_type()
    
    run_experiments(cause_column, effect_column, ds_path, result_path, col_list, experiment_type)

def large_trafic_experiment(col_list):
    cause_column, effect_column = get_cause_effect_col()
    ds_path = get_large_traffic()
    result_path = get_result_path()
    experiment_type = get_large_trafic_exp_type()
    
    run_experiments(cause_column, effect_column, ds_path, result_path, col_list, experiment_type)

def test_cluster():
    pass

def small_traffic_cluster():
    pass

def test_experiment():
    pass


if __name__ == '__main__':
    start_time = time.time()
    
    user_input = get_userinput()
    cluster_colum = 'traffic_volume'
    col_list = ['weather_main','weather_description','weather_description_cluster']
    
    if user_input == 'cluster':
        run_cluster(cluster_colum)
    elif user_input == 'experiment':
        small_trafic_experiment(col_list)
    elif user_input == '':
        run_cluster(cluster_colum)
        small_trafic_experiment(col_list)
    else:
        print("The given input was not valid.\nThe program will now exit.")
    
    print("--- %s seconds ---" % (time.time() - start_time))