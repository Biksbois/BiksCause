from BiksCalculations.CIR import *
from BiksCalculations.NST import *
from BiksCalculations.dataset_object import *
from BiksCalculations.optimizer import *
import multiprocessing

from tqdm import tqdm

def calculate(x, y, ds_obj, matrixes, suf_dict, nec_dict, d_dict, alpha_val = 0.66, lambda_val = 0.5):
    nst = get_nst(ds_obj, alpha_val, lambda_val, x, y, nec_dict=nec_dict, suf_dict=suf_dict)
    cir_c = calc_cir_c(ds_obj, x, y, big_dict=nec_dict, d_dict=d_dict)
    cir_b = calc_cir_b(ds_obj, x, y, big_dict=nec_dict, d_dict=d_dict)
    
    matrixes['nst'].xs(x)[y] = round(nst, 2)
    matrixes['cir_c'].xs(x)[y] = round(cir_c, 2)
    matrixes['cir_b'].xs(x)[y] = round(cir_b, 2)

def extract_values(colum_list, colum_dict):
    vals_to_check = []
    for key in colum_list:
        vals_to_check.extend(colum_dict[key].keys())
    return vals_to_check

def create_datafram_matric(distinct_values, save_index):
    test_data = [["" for i in range(len(distinct_values))] for i in range(len(distinct_values))]
    data_matrix = pd.DataFrame(test_data, columns = distinct_values, index=distinct_values)
    return data_matrix

def create_matix_path(s, base_path, experiment_type):
    return f'{base_path}/{experiment_type}_{s}_matrix.csv'
    # return f'BiksCalculations/results/{s}_matrix.csv'

def init_matrixes(scores, distinct_values, base_path, experiment_type):
    matrix_dict = {}
    for s in scores:
        save_path = create_matix_path(s, base_path, experiment_type)
        matrix_dict[s] = create_datafram_matric(distinct_values, save_path)
    return matrix_dict

def do_calculations(ds_obj, cause_column, effect_column, base_path, colum_list, experiment_type, csv_path, use_optimizer=True):
    scores = ['nst', 'cir_c', 'cir_b']

    # ds_obj = init_obj_test(cause_column=cause_column, effect_column=effect_column)
    ds_obj = init_obj_test_trafic(cause_column=cause_column, effect_column=effect_column)

    
    colum_dict = {}
    
    for c in colum_list:
        colum_dict[c] = ds_obj.create_dict(c)
    
    distinct_values = extract_values(colum_list, colum_dict)
    
    matrixes = init_matrixes(scores, distinct_values, base_path, experiment_type)

    if use_optimizer:
        suf_dict, nec_dict, d_dict = generate_lookup_dict(colum_list ,ds_obj)
    else:
        suf_dict = {}
        nec_dict = {}
        d_dict = {}
    mat_list = list(Threading_max(colum_list,colum_dict,ds_obj, matrixes,suf_dict, nec_dict, d_dict))
    res = []
    #pd.concat([df1,df2], ignore_index=False)
    tl = pd.merge(mat_list[0]['nst'],mat_list[1]['nst'], how='right', on=['Clouds','Clear'])
    
    save_path = create_matix_path('cir_b', base_path, experiment_type+'yeet')
    tl.to_csv(save_path, index=True, header=True)
    
    for s in scores:
        save_path = create_matix_path(s, base_path, experiment_type)
        matrixes[s].to_csv(save_path, index=True, header=True)
def Threading_max(lst, dic, ds_obj, matrixes, suf_dict, nec_dict, d_dict):
    lsts = []
    progs = []
    matris = []
    manager = multiprocessing.Manager()
    shared_dict = manager.list()
    
    for l in List_spliter(lst,3):
        lsts.append(l)
    for ls in lsts:
        p = multiprocessing.Process(target=calc_procces, args=(ls,lst,dic,ds_obj,matrixes,suf_dict,nec_dict,shared_dict,d_dict))
        p.start()
        progs.append(p)
    #p = Process(target=f, args=('bob',))
    #p.start()
    for pro in progs:
        pro.join()
    return shared_dict
        
def calc_procces(lst,colum_list, colum_dict, ds_obj, matrixes, suf_dict, nec_dict, ret_dict,d_dict):
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
                    calculate(e, c, ds_obj, matrixes, suf_dict, nec_dict,d_dict)
        #ret_dict = {**ret_dict, **matrixes}
    ret_dict.append(matrixes)
