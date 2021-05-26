from BiksCalculations.dataset_object import *

def calc_cir_m_nom(x, y, z, big_dict, d_dict, ds_obj):
    if y == z:
        key = y
    else:
        key = sorted([y, z])
    
    n = ds_obj.get_n_cir_m(x, key, big_dict=big_dict)
    d = ds_obj.get_d_cir_m(x, key, d_dict=d_dict)
    
    if d == 0:
        return 0
    else:
        return n / d

def calc_cir_m_den(x, y, z, big_dict, d_dict, ds_obj):
    key = sorted([y, z])
    if y == z:
        return 0
        # key[0] = f"not_{key[0]}"
    else:
        key = [w.replace(y, f"not_{y}") for w in key]
    
    n = ds_obj.get_n_cir_m(x, key, big_dict=big_dict)
    d = ds_obj.get_d_cir_m(x, key, d_dict=d_dict)
    
    if d == 0:
        return 0
    else:
        return n / d

def calc_cir_m(x, y, z, big_dict, d_dict, ds_obj):
    cir_m_nom = calc_cir_m_nom(x, y, z, big_dict, d_dict, ds_obj)
    cir_m_den = calc_cir_m_den(x, y, z, big_dict, d_dict, ds_obj)
    
    if cir_m_den == 0:
        return 0
    else:
        return cir_m_nom / cir_m_den

def calc_cir_m_avg_max(x, y, z_set, big_dict, d_dict, ds_obj):
    result_list = []
    
    for z in z_set:
        result_list.append(calc_cir_m(x, y, z, big_dict, d_dict, ds_obj))
    
    # print("\n\n\n---\n")
    # print(result_list)
    
    avg_res = sum(result_list) / len(result_list)
    max_res = max(result_list) 
    min_res = max_res
    
    for num in result_list:
        if min_res > num and not num == 0:
            min_res = num
    
    # print(f"avg res: {avg_res}")
    # print(f"max res: {max_res}")
    # print(f"min res: {min_res}")
    
    # print(big_dict)
    # print('\n\n\n\n-------------------------\n\n\n\n')
    # print(d_dict)
    # exit()
    
    return avg_res, max_res, min_res

def cir_nom(ds_obj, x, y, big_dict=None, d_dict=None):
    n = ds_obj.get_n(x, y, big_dict=big_dict) #ds_obj.calc_n(y, x)
    d = ds_obj.get_d(y, d_dict=d_dict)
    
    if n == 0 or d == 0:
        return 0
    else:
        return n / d

def cir_b_den(ds_obj, x):
    return ds_obj.calc_effect_prob(x)

def cir_c_den_nom(ds_obj, x, y, big_dict=None):
    n = ds_obj.get_n(x, y, big_dict=big_dict)
    return ds_obj.effect_dict[x] - n # ds_obj.calc_n(y, x)

def cir_c_den_den(ds_obj, x, y, d_dict=None):
    return ds_obj.get_col_len() - ds_obj.get_d(y, d_dict=d_dict)

def cir_c_den(ds_obj, x, y, big_dict=None, d_dict=None):
    return cir_c_den_nom(ds_obj, x, y, big_dict=big_dict) / cir_c_den_den(ds_obj, x, y, d_dict=d_dict)

def calc_cir_b(ds_obj, x, y, big_dict=None, d_dict=None):
    return cir_nom(ds_obj, x, y, big_dict=big_dict, d_dict=d_dict) / cir_b_den(ds_obj, x)

def calc_cir_c(ds_obj, x, y, big_dict=None, d_dict=None):
    nom = cir_nom(ds_obj, x, y, big_dict=big_dict, d_dict=d_dict)
    den = cir_c_den(ds_obj, x, y, big_dict=big_dict, d_dict=d_dict)

    
    
    if den == 0:
        return 0
    else:
        return nom / den

if __name__ == '__main__':
    ds_obj = init_obj_test()