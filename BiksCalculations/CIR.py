from BiksCalculations.dataset_object import *
import sys



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