from BiksCalculations.CIR import *
from BiksCalculations.NST import *
from BiksCalculations.dataset_object import *
from BiksCalculations.optimizer import *
from experiment_obj import exp_obj
import multiprocessing
from functools import reduce

from tqdm import tqdm

def calculate(x, y, ds_obj, matrixes, suf_dict, nec_dict, d_dict, e_obj):
    nst = get_nst_dict(ds_obj, e_obj, x, y, nec_dict=nec_dict, suf_dict=suf_dict)
    cir_c = calc_cir_c(ds_obj, x, y, big_dict=nec_dict, d_dict=d_dict)
    cir_b = calc_cir_b(ds_obj, x, y, big_dict=nec_dict, d_dict=d_dict)
    
    for key in e_obj.nst_keys:
        # if nst[key] > 0:
        matrixes[key].xs(x)[y] = round(nst[key], 2)
    
    # if cir_c > 0:
    matrixes['cir_c'].xs(x)[y] = round(cir_c, 2)
    # if cir_b > 0:
    matrixes['cir_b'].xs(x)[y] = round(cir_b, 2)

def extract_values(colum_list, colum_dict):
    vals_to_check = []
    for key in colum_list:
        vals_to_check.extend(colum_dict[key].keys())
    return vals_to_check

def create_datafram_matric(distinct_values, save_index):
    test_data = [[0.0 for i in range(len(distinct_values))] for i in range(len(distinct_values))]
    data_matrix = pd.DataFrame(test_data, columns = distinct_values, index=distinct_values)
    return data_matrix

def create_matix_path(s, base_path, e_obj):
    return f'{base_path}/{e_obj.exp_type}_{s}_h{e_obj.head_val}_w{e_obj.window_size}_matrix.csv'

def init_matrixes(scores, distinct_values, base_path, e_obj):
    matrix_dict = {}
    for s in scores:
        save_path = create_matix_path(s, base_path, e_obj)
        matrix_dict[s] = create_datafram_matric(distinct_values, save_path)
    return matrix_dict

def Construct_Result_Table(dts):
    result = {}
    for i in range(len(dts)):
        for exp in dts[i].keys():
            if not exp in result:
                result[exp] = []
            result[exp].append(dts[i][exp])
    
    for key in result.keys():
        result[key] = reduce(lambda x, y: x.add(y, fill_value=0), result[key])
        result[key] = result[key].replace(0.0, '')
    
    return result

def remove_columes(df,lst):
    return df.drop(columns=lst)

def do_calculations(ds_obj, cause_column, effect_column, base_path, colum_list, ds_path, e_obj, use_optimizer=True):
    scores = ['cir_c', 'cir_b']
    scores.extend(e_obj.nst_keys)
    
    colum_dict = {}
    
    for c in colum_list:
        colum_dict[c] = ds_obj.create_dict(c)
    
    distinct_values = extract_values(colum_list, colum_dict)
    
    matrixes = init_matrixes(scores, distinct_values, base_path, e_obj)

    # print(f"MATRICES FROM INIT MATRIXES\n{matrixes}")
    
    if use_optimizer:
        suf_dict, nec_dict, d_dict = generate_lookup_dict(colum_list ,ds_obj, e_obj.support)
    else:
        suf_dict = None
        nec_dict = None
        d_dict = None
    
    mat_list = list(Threading_max(colum_list, colum_dict, ds_obj, matrixes, suf_dict, nec_dict, d_dict, e_obj))
    
    res = []
    # try:
    matrixes = Construct_Result_Table(mat_list)
    
    # print(f"MATRICES FROM Construct_Result_Table\n{matrixes}")
    
    # except Exception as e:
    #     print(f"\n---\nERROR: {e}\nThe program was unable to save.\n---\n\n")

    for s in scores:
        save_path = create_matix_path(s, base_path, e_obj)
        matrixes[s].to_csv(save_path, index=True, header=True)

def Threading_max(lst, dic, ds_obj, matrixes, suf_dict, nec_dict, d_dict, e_obj, core_count = 3):
    lsts = []
    progs = []
    matris = []
    manager = multiprocessing.Manager()
    shared_dict = manager.list()
    
    for l in List_spliter(lst,core_count):
        lsts.append(l)
    for ls in lsts:
        p = multiprocessing.Process(target=calc_procces, args=(ls,lst,dic,ds_obj,matrixes,suf_dict,nec_dict,shared_dict,d_dict, e_obj))
        p.start()
        progs.append(p)

    for pro in progs:
        pro.join()
    return shared_dict

def calc_procces(lst,colum_list, colum_dict, ds_obj, matrixes, suf_dict, nec_dict, ret_dict,d_dict, e_obj):
    for i in tqdm(range(len(lst))):
        cause = lst[i]
        ds_obj.cause_dict = colum_dict[cause]
        ds_obj.cause_column = cause

        for j in tqdm(range(len(colum_list))):
            effect = colum_list[j]
            ds_obj.effect_dict = colum_dict[effect]
            
            ds_obj.effect_column = effect
            
            for c in colum_dict[cause]:
                for e in colum_dict[effect]:
                    calculate(e, c, ds_obj, matrixes, suf_dict, nec_dict,d_dict, e_obj)
    
    ret_dict.append(matrixes)
