import sys
from BiksCalculations.Matrix_clarify.Matrix_obj import get_at_k_hits, run_average_expriment, air_experiment_results
import itertools
import time
import pandas as pd
import datetime
from experiment_obj import *
from BiksPrepare.duration_method import generate_clusters
from BiksCalculations.calc_main import do_calculations
from BiksCalculations.dataset_object import init_obj_test_trafic
from main_paths import *
from BiksCalculations.find_potential_parents import *
from BiksPrepare.synthetic_generator import initiate_generation, cluster_class

def get_userinput(head_val_small, head_val_large, large, traffic, synthetic, power, *argv):
    if len(sys.argv) >= 2:
        is_large = large in str(sys.argv[1:])
        
        if is_large:
            head_val = head_val_large
        else:
            head_val = head_val_small
        
        exp_type = ''
        
        if synthetic in sys.argv[1:]:
            exp_type = synthetic
        if power in sys.argv[1:]:
            exp_type = power
        if traffic in sys.argv[1:]:
            exp_type = traffic
        
        # is_traffic = not test in str(sys.argv[1:])
        
        written_args = [x for x in sys.argv[1:] if x in argv]
        
        return exp_type, head_val, written_args
    else:
        return '', head_val_small, []

def run_cluster(ds_path, cluster_colum, is_cluster_numbers, time_colum, temp_csv_path):
    generate_clusters(ds_path, cluster_colum, is_cluster_numbers, time_colum, temp_csv_path)

def run_experiments(ds_obj, cause_column, effect_column, ds_path, result_path, cluster_col, baseline_col, e_obj, window_size, index, use_optimizer=True, hardcoded_cir_m=None):
    for w in window_size:
        e_obj.window_size = w
        ds_obj.window_size = w
        
        if not hardcoded_cir_m == None and w in hardcoded_cir_m:
            print(f"The CIR_m parent dictionary has been updated to key '{w}'.")
            ds_obj.hardcoded_cir_m = hardcoded_cir_m[w]
        else:
            ds_obj.hardcoded_cir_m = None
        
        print(f"---\nThe experiments with clusters will now run for window size {w}\n---", flush=True)
        do_calculations(ds_obj, cause_column, effect_column, f"{result_path}/cluster/{index}_", cluster_col, ds_path, e_obj, use_optimizer=use_optimizer)

        print(f"---\nThe experiments without clusters will now run for window size {w}\n---", flush=True)
        do_calculations(ds_obj, cause_column, effect_column, f"{result_path}/no_cluster/{index}_", baseline_col, ds_path, e_obj, use_optimizer=use_optimizer)
    
    print("\nThe experiments are now successfully done, and the program will exit.")


def get_exp_type(ds_pat):
    if 'summer' in ds_pat:
        return f'{power}_summer'
    if 'winter' in ds_pat:
        return f'{power}_winter'
    if 'fall' in ds_pat:
        return f'{power}_fall'
    if 'spring' in ds_pat:
        return f'{power}_spring'
    else:
        print(f"ERROR: no season was in {ds_pat}")
        return f'{power}'

def call_experiment(e_obj, data_obj, window_size, exp_type):
    for p in range(len(data_obj.ds_path)):
        ds_obj = init_obj_test_trafic(cause_column=data_obj.cause_column, effect_column=data_obj.effect_column, 
                                    ds_path=data_obj.ds_path[p], windows_size=window_size, head_val=e_obj.head_val, time_column=data_obj.time_colum)
        
        if exp_type == power:
            e_obj.exp_type = get_exp_type(data_obj.ds_path[p])
        
        # print(f"new path is now: {e_obj.exp_type}")
        
        run_experiments(ds_obj, data_obj.cause_column, data_obj.effect_column, data_obj.ds_path[p], 
                        data_obj.result_path, data_obj.cluster_col_names, data_obj.baseline_col_names, 
                        e_obj, window_size, p, hardcoded_cir_m=data_obj.hardcoded_cir_m)

def test_cluster():
    pass

def print_not_implemented(message):
    print(f"\n\n---{message}, this feature has not been implemented yet.\n---\n")

def large_medical_experiment(cluster_col, baseline_col, e_obj, window_size):
    pass

def print_start(exp_name, head_val, exp_type, window_size, lambda_val, alpha_val, support, scores):
    print(f"---\nThe experiment with the following input will now run:" + 
            f"\n  - type: {exp_name}\n  - size: {head_val}\n  - {exp_type}\n" + 
            f"- windowsize: {window_size}\n" + 
            f"- alpha values: {alpha_val}\n  - lambda values: {lambda_val}\n  - support: {support}")
    print("  - scores:")
    for s in scores:
        print(f"    - {s}")

def print_scores(scores, window_size, head_val, result_path, k_vals, extensions):
    # extensions = ['cluster', 'no_cluster']
    
    for e in extensions:
        full_path = f"{result_path}\\{e}"
        print(full_path)
        for k in k_vals:
            for s in scores:
                #k_hit = get_at_k_hits(full_path, k, s, f"traffic_{e}", window=window_size, heads=[head_val])
                # print(f'The Value of k dontes a new eperiment:{k}')
                # print(s)
                # air_experiment_results(full_path, k, s, get_ground_truth())
                print(run_average_expriment(full_path, k, s, get_ground_truth(), window=window_size, heads=[head_val]))
                # print(f"---\nScore: {s}\n  - k@hit = {k_hit}\n  - k = {k}\n  - mode = {e}")

def call_cluster(e_obj, data_obj):
    for ds_path in data_obj.ds_path:
        for c in data_obj.cluster_colums:
            is_number = c[1]
            col_name = c[0]
            
            run_cluster(ds_path, col_name, is_number, data_obj.time_colum, data_obj.temp_csv_path)

def get_ground_truth():
    return {
        'a_0': cluster_class((6,10), ['b_0'], [0.8]),
        'a_1': cluster_class((30,36), ['b_1'], [0.8]),
        'a_2': cluster_class((70,75), ['b_1'], [0.8]),
        'b_0': cluster_class((3,4), ['c_0'], [0.8]),
        'b_1': cluster_class((10,12), ['c_1'], [0.8]),
        'b_2': cluster_class((21,23), ['c_2'], [0.8]),
        'c_0': cluster_class((1,4), ['e_0'], [0.8]),
        'c_1': cluster_class((15,18), ['d_0'], [0.8]),
        'c_2': cluster_class((31,34), ['d_0'], [0.8]),
        'd_0': cluster_class((5,12), ['e_0'], [0.8]),
        'e_0': cluster_class((2,5), [''], [0])
    }

def get_current_season(dongsi_seasons, m):
    for s in dongsi_seasons:
        if m in s[1]:
            return s[0]

def generate_dataset(years, dataset_count, window_size, exp_type):
    if exp_type == synthetic:
        for i in range(dataset_count):
            events = get_ground_truth()
            
            output_path = f'output_csv//generated_data//gen_{i}.csv'
            
            initiate_generation(output_path, events, years, window_size)
    if exp_type == power:
        dongsi_seasons = [('spring', [3,4,5]), ('summer', [6,7,8]), ('fall', [9,10,11]), ('winter', [12,1,2])]
        dongsi_dict = {x[0]:([], f"input_csv\PRSA_Data_Dongsi_{x[0]}.csv") for x in dongsi_seasons}
        pd_dict = {x[0]:pd.read_csv(dongsi_dict[x[0]][1]) for x in dongsi_seasons}
        
        ds_path = 'input_csv\PRSA_Data_Dongsi_20130301-20170228.csv'
        df = pd.read_csv(ds_path)
        val_list = df['time_set'].tolist()
        current_season = ''
        start = 0
        end = 0
        
        for i in range(len(val_list)):
            date_time_obj = datetime.datetime.strptime(val_list[i], '%Y-%m-%d %H:%M:%S')
            m = date_time_obj.month
            
            temp_season = get_current_season(dongsi_seasons, m)
            
            if current_season == '':
                current_season = temp_season
                start = i
            
            elif not temp_season == current_season:
                end = i - 1
                dongsi_dict[current_season][0].append([start, end])
                current_season = ''
        
        for key in dongsi_dict.keys():
            for r in dongsi_dict[key][0]:
                print(type(pd_dict[key]))
                pd_dict[key] = pd.concat([pd_dict[key], df[r[0]:r[1]]], ignore_index=True)
        
        for key in pd_dict.keys():
            print(pd_dict[key])
            pd_dict[key].to_csv(dongsi_dict[key][1])

def run_experiment(arg, written_args, run_everything):
    if arg in written_args or run_everything in written_args:
        return True
    else:
        return False

def init_exp_obj(head_val, exp_type, alpha_val, lambda_val, window_size, support, scores):
    return exp_obj(alpha_val, lambda_val, window_size, head_val, exp_type, head_val, support, scores)

# Parameters for what dataset to use
traffic = 'traffic'
synthetic = 'synthetic'
power = 'air'

if __name__ == '__main__':
    start_time = time.time()
    
    # Parameters for what to input when deciding size of csv
    large = 'large'
    small = 'small'
    
    
    # Parameters for what to run
    cluster = 'cluster'
    experiment = 'experiment'
    result = 'result'
    generate = 'generate'
    run_everythin = 'all'
    
    # Parameters for csv size
    head_val_small = 5
    head_val_large = 50000
    
    # Parameters for CEAS scores
    window_size = [1, 5, 10, 6, 12, 18, 24]
    alpha_val = [0.55, 0.66, 0.77]
    lambda_val = [0.4, 0.5, 0.7]
    
    k_vals = [10, 15, 20, 25]
    extensions = ['cluster', 'no_cluster']
    
    # Parameters for generating dataset
    dataset_count = 100
    years = 1000
    gen_window_size = 5
    
    # The scres to calculate
    scores = ['cir_c', 'cir_b', 'cir_m_avg', 'cir_m_max', 'cir_m_min'] # More keys are added in the constructor

    # How to group the scores when finding best result
    scores_short = ['cir_c', 'cir_b', 'nst']
    
    
    support = 10
    
    exp_type, head_val, written_args = get_userinput(head_val_small, head_val_large, large, traffic, synthetic, power, cluster, experiment, result, generate, run_everythin)
    
    if exp_type == '':
        print(f"\n\n---\nPlease input what dataset to run on.\nThis can be either:\n  - {traffic}\n  - {synthetic}\n  - {power}\n\n---")
    elif len(written_args) == 0:
        print(f"\n\n---\n\nPlease input what experiments to run.\nThis can be either:\n  - {cluster}: if you wish to create new clusters\n  - {experiment}: if you wish to run the experiments\n  - {result}: If you wish to see the results\n  - {generate}: if you wish to generate new datasets\n  - {run_everythin}: if you wish to run everything")
    else:
        e_obj = exp_obj(alpha_val, lambda_val, window_size, head_val, exp_type, head_val, support, scores)
        data_obj = get_datatype(exp_type)
        
        if run_experiment(generate, written_args, run_everythin):
            print("\n---\nNew datasets are being generated...\n---\n", flush=True)
            generate_dataset(years, dataset_count, gen_window_size, exp_type)
        
        if run_experiment(cluster, written_args, run_everythin):
            print(f"\n---\nClusters are being generated for {e_obj.exp_type}\n---\n", flush=True)
            call_cluster(e_obj, data_obj)
        
        if run_experiment(experiment, written_args, run_everythin):
            print_start(exp_type, head_val, written_args, window_size, lambda_val, alpha_val, support, e_obj.scores)
            call_experiment(e_obj, data_obj, window_size, exp_type)
        
        if run_experiment(result, written_args, run_everythin):
            print("\n---\nThe result scores are being estimated...\n---\n", flush=True)
            print_scores(scores_short, window_size, head_val, data_obj.result_path, k_vals, extensions)
    
    
    print("\nThe program will now exit.\n")
    print("\n\n--- %s seconds ---\n\n" % round((time.time() - start_time), 2))