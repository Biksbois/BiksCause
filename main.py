import sys
import time

from BiksPrepare.duration_method import generate_clusters
from BiksCalculations.calc_main import do_calculations
from BiksCalculations.dataset_object import init_obj_test_trafic

ds_path = u'input_csv\Metro_Interstate_Traffic_Volume.csv'
# ds_path = u'BiksCalculations\csv\\ny_trafic.csv'
time_colum = 'date_time'
temp_csv_path = u'BiksCalculations\csv\\temp_csv'
col_list = ['weather_main','weather_description','weather_description_cluster'] # 
cause_column = 'weather_description'
effect_column = 'weather_description'
experiment_type = 'ny_traffic'
result_path = 'BiksCalculations/results'

def get_userinput():
    if len(sys.argv) >= 2:
        return str(sys.argv[1])
    else:
        return ''

def run_cluster(cluster_colum):
    generate_clusters(ds_path, cluster_colum, time_colum, temp_csv_path)

def run_experiments(use_optimizer=True):
    ds_obj = init_obj_test_trafic(cause_column=cause_column, effect_column=effect_column, ds_path=ds_path)

    do_calculations(ds_obj, cause_column, effect_column, result_path, col_list, experiment_type, ds_path, use_optimizer=use_optimizer)
    print("The experiments are now successfully done, and the program will exit.")

if __name__ == '__main__':
    start_time = time.time()
    
    user_input = get_userinput()
    cluster_colum = 'traffic_volume'
    
    if user_input == 'cluster':
        run_cluster(cluster_colum)
    elif user_input == 'experiment':
        run_experiments()
    elif user_input == '':
        run_cluster(cluster_colum)
        run_experiments()
    else:
        print("The given input was not valid.\nThe program will now exit.")
    
    print("--- %s seconds ---" % (time.time() - start_time))