import sys
import time

from BiksPrepare.duration_method import generate_clusters
from BiksCalculations.calc_main import do_calculations

def get_userinput():
    if len(sys.argv) >= 2:
        return str(sys.argv[1])
    else:
        return ''

def run_cluster():
    ds_path = u'input_csv\Metro_Interstate_Traffic_Volume.csv'
    colum = 'weather_description'
    time_colum = 'date_time'
    temp_csv_path = u'BiksCalculations\csv\\temp_csv'
    
    generate_clusters(ds_path, colum, time_colum, temp_csv_path)

# def run_experiments():
#     cause_column = 'label'
#     effect_column = 'label'
#     colum_list = ['label', 'test','dur_cluster']
#     base_path = 'BiksCalculations/results'

#     do_calculations(cause_column, effect_column, base_path, colum_list)
#     print("The experiments are now successfully done, and the program will exit.")

def run_experiments():
    cause_column = 'weather_description'
    effect_column = 'weather_description'
    colum_list = ['weather_main','weather_description','weather_description_cluster']
    base_path = 'BiksCalculations/results'
    experiment_type = 'ny_traffic'

    do_calculations(cause_column, effect_column, base_path, colum_list, experiment_type)
    print("The experiments are now successfully done, and the program will exit.")

if __name__ == '__main__':
    start_time = time.time()
    
    user_input = get_userinput()
    
    if user_input == 'cluster' or user_input == '':
        run_cluster()
    elif user_input == 'experiment':
        run_experiments()
    elif user_input == '':
        run_cluster()
        run_experiments()
    else:
        print("The given input was not valid.\nThe program will now exit.")
    
    print("--- %s seconds ---" % (time.time() - start_time))