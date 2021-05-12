import sys
from BiksCalculations.Matrix_clarify.Matrix_obj import get_at_k_hits
import itertools
import time
import pandas as pd
from experiment_obj import *
from BiksPrepare.duration_method import generate_clusters
from BiksCalculations.calc_main import do_calculations
from BiksCalculations.dataset_object import init_obj_test_trafic
from main_paths import *
from BiksCalculations.find_potential_parents import *
from BiksPrepare.synthetic_generator import initiate_generation

def get_userinput(head_val_small, head_val_large, large, traffic, synthetic, *argv):
    if len(sys.argv) >= 2:
        is_large = large in str(sys.argv[1:])
        
        if is_large:
            head_val = head_val_large
        else:
            head_val = head_val_small
        
        if synthetic in sys.argv[1:]:
            exp_type = synthetic
        else:
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

def call_experiment(e_obj, data_obj, window_size):
    for p in range(len(data_obj.ds_path)):
        ds_obj = init_obj_test_trafic(cause_column=data_obj.cause_column, effect_column=data_obj.effect_column, 
                                    ds_path=data_obj.ds_path[p], windows_size=window_size, head_val=e_obj.head_val, time_column=data_obj.time_colum)
        
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

def print_scores(scores, window_size, head_val):
    result_path = get_result_path()
    extensions = ['cluster', 'no_cluster']
    k_vals = [10, 15, 20]
    
    for e in extensions:
        full_path = f"{result_path}\\{e}"
        for k in k_vals:
            for s in scores:
                k_hit = get_at_k_hits(full_path, k, s, f"traffic_{e}", window=window_size, heads=[head_val])
                print(f"---\nScore: {s}\n  - k@hit = {k_hit}\n  - k = {k}\n  - mode = {e}")

def call_cluster(e_obj, data_obj):
    for ds_path in data_obj.ds_path:
        for c in data_obj.cluster_colums:
            is_number = c[1]
            col_name = c[0]
            
            run_cluster(ds_path, col_name, is_number, data_obj.time_colum, data_obj.temp_csv_path)

def generate_dataset():
    
    for i in range(2):
        events = {'a': [['a',0],['b',0.5],['c',0]],
            'b': [['a',0],['b',0],['c',0.5]],
            'c': [['a',0.5],['b',0],['c',0]]}
        
        output_path = f'output_csv//generated_data//gen_{i}.csv'
        
        years = 1
        win_size = 5
        
        initiate_generation(output_path, events = events, years = years, win_size = win_size)

def run_experiment(arg, written_args):
    if arg in written_args or len(written_args) == 0:
        return True
    else:
        return False

def init_exp_obj(head_val, exp_type, alpha_val, lambda_val, window_size, support, scores):
    return exp_obj(alpha_val, lambda_val, window_size, head_val, exp_type, head_val, support, scores)

if __name__ == '__main__':
    start_time = time.time()
    
    large = 'large'
    small = 'small'
    
    traffic = 'traffic'
    synthetic = 'synthetic'
    power = 'power'
    
    cluster = 'cluster'
    experiment = 'experiment'
    result = 'result'
    generate = 'generate'
    
    head_val_small = 1000
    head_val_large = 50000
    
    window_size = [1, 5, 10, 6, 12, 18, 24]
    alpha_val = [0.55, 0.66, 0.77]
    lambda_val = [0.4, 0.5, 0.7]
    
    scores = ['cir_c', 'cir_b', 'cir_m_avg', 'cir_m_max', 'cir_m_min'] # More keys are added in the constructor
    scores_short = ['cir_c', 'cir_b', 'cir_m_avg', 'cir_m_max', 'cir_m_min', 'nst']
    
    support = 10
    
    exp_type, head_val, written_args = get_userinput(head_val_small, head_val_large, large, traffic, synthetic, cluster, experiment, result, generate)

    if exp_type == '':
        print(f"\n\n---\nPlease input what dataset to run on.\nThis can be either:\n  - {traffic}\n  - {synthetic}\n  - {power}\n\n---")
    else:
        e_obj = exp_obj(alpha_val, lambda_val, window_size, head_val, exp_type, head_val, support, scores)
        data_obj = get_datatype(exp_type)
        
        if run_experiment(generate, written_args):
            print("\n---\nNew datasets are being generated...\n---\n", flush=True)
            generate_dataset()
        if run_experiment(cluster, written_args):
            print(f"\n---\nClusters are being generated for {e_obj.exp_type}\n---\n", flush=True)
            call_cluster(e_obj, data_obj)
        if run_experiment(experiment, written_args):
            print_start(exp_type, head_val, written_args, window_size, lambda_val, alpha_val, support, e_obj.scores)
            call_experiment(e_obj, data_obj, window_size)
        if run_experiment(result, written_args):
            print("\n---\nThe result scores are being estimated...\n---\n", flush=True)
            print_scores(scores_short, window_size, head_val_large if is_large else head_val_small)
    
    
    print("\nThe program will now exit.\n")
    print("\n\n--- %s seconds ---\n\n" % round((time.time() - start_time), 2))