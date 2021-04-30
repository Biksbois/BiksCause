import multiprocessing
from optimizer import *
from dataset_object import *
from calc_main import calculate
import pandas as pd
from tqdm import tqdm


def init_obj_test_trafic(cause_column='weather_description', effect_column='weather_description', time_column='date_time', head_val = -1, windows_size = 3, ds_path=''):
    window_size = windows_size
    # col_name = 'weather_description'
    # if ds_path == '':   
    ds_path = "BiksCalculations\csv\\ny_trafic.csv"

    return dataset(ds_path, cause_column, effect_column , window_size,date_window_method, time_column, head_val = head_val)

test = init_obj_test_trafic();
def create_datafram_matric(distinct_values, save_index):
    test_data = [["" for i in range(len(distinct_values))] for i in range(len(distinct_values))]
    data_matrix = pd.DataFrame(test_data, columns = distinct_values, index=distinct_values)
    return data_matrix
def create_matix_path(s, base_path, experiment_type):
    return f'{base_path}/{experiment_type}_{s}_matrix.csv'
    # return f'BiksCalculations/results/{s}_matrix.csv'
def extract_values(colum_list, colum_dict):
    vals_to_check = []
    for key in colum_list:
        vals_to_check.extend(colum_dict[key].keys())
    return vals_to_check
def init_matrixes(scores, distinct_values, base_path, experiment_type):
    matrix_dict = {}
    for s in scores:
        save_path = create_matix_path(s, base_path, experiment_type)
        matrix_dict[s] = create_datafram_matric(distinct_values, save_path)
    return matrix_dict

def do_calculations(cause_column, effect_column, base_path, colum_list, experiment_type):
    scores = ['nst', 'cir_c', 'cir_b']

    # ds_obj = init_obj_test(cause_column=cause_column, effect_column=effect_column)
    ds_obj = init_obj_test_trafic(cause_column=cause_column, effect_column=effect_column)

    
    colum_dict = {}
    
    for c in colum_list:
        colum_dict[c] = ds_obj.create_dict(c)
    
    distinct_values = extract_values(colum_list, colum_dict)
    
    matrixes = init_matrixes(scores, distinct_values, base_path, experiment_type)

    suf_dict, nec_dict = generate_lookup_dict()
    mat_list = list(Threading_max(colum_list,colum_dict,ds_obj, matrixes,suf_dict, nec_dict))
    res = []
    #pd.concat([df1,df2], ignore_index=False)
    tl = pd.merge(mat_list[0]['nst'],mat_list[1]['nst'], how='right', on=['Clouds','Clear'])
    
    save_path = create_matix_path('cir_b', base_path, experiment_type+'yeet')
    tl.to_csv(save_path, index=True, header=True)
    
    for s in scores:
        save_path = create_matix_path(s, base_path, experiment_type)
        matrixes[s].to_csv(save_path, index=True, header=True)
def Threading_max(lst, dic, ds_obj, matrixes, suf_dict, nec_dict):
    lsts = []
    progs = []
    matris = []
    manager = multiprocessing.Manager()
    shared_dict = manager.list()
    
    for l in List_spliter(lst,3):
        lsts.append(l)
    for ls in lsts:
        p = multiprocessing.Process(target=calc_procces, args=(ls,lst,dic,ds_obj,matrixes,suf_dict,nec_dict,shared_dict))
        p.start()
        progs.append(p)
    #p = Process(target=f, args=('bob',))
    #p.start()
    for pro in progs:
        pro.join()
    return shared_dict
        
def calc_procces(lst,colum_list, colum_dict, ds_obj, matrixes, suf_dict, nec_dict, ret_dict):
    for i in tqdm(range(len(lst))):
        cause = lst[i]
        ds_obj.cause_dict = colum_dict[cause]
        ds_obj.cause_column = cause

        # for effect in colum_list:
        for j in tqdm(range(len(colum_list))):
            effect = colum_list[j]
            ds_obj.effect_dict = colum_dict[effect]
            
            ds_obj.effect_column = effect
            
            for c in colum_dict[cause]:
                for e in colum_dict[effect]:
                    calculate(e, c, ds_obj, matrixes, suf_dict, nec_dict)
        #ret_dict = {**ret_dict, **matrixes}
    ret_dict.append(matrixes)


def run_experiments():
    cause_column = 'weather_description'
    effect_column = 'weather_description'
    colum_list = ['weather_main', 'weather_description', 'weather_description_cluster']
    base_path = 'BiksCalculations/results'
    experiment_type = 'ny_traffic'

    do_calculations(cause_column, effect_column, base_path, colum_list, experiment_type)
    print("The experiments are now successfully done, and the program will exit.")

if __name__ == '__main__':
    run_experiments()
    print('yeet')