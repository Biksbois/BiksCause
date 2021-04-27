from BiksCalculations.dataset_object import *

def get_n(ds_obj, x, y, big_dict={}):
    if x in big_dict and y in big_dict[x]:
        return big_dict[x][y]
    else:
        return ds_obj.calc_n(y, x)

def cir_nom(ds_obj, x, y, big_dict={}):
    n = get_n(ds_obj, x, y, big_dict=big_dict) #ds_obj.calc_n(y, x)
    d = ds_obj.calc_d(y)
    return n / d

def cir_b_den(ds_obj, x):
    return ds_obj.calc_effect_prob(x)

def cir_c_den_nom(ds_obj, x, y, big_dict={}):
    n = get_n(ds_obj, x, y, big_dict=big_dict)
    return ds_obj.effect_dict[x] - n # ds_obj.calc_n(y, x)

def cir_c_den_den(ds_obj, x, y):
    return ds_obj.get_col_len() - ds_obj.calc_d(y)

def cir_c_den(ds_obj, x, y, big_dict={}):
    return cir_c_den_nom(ds_obj, x, y, big_dict=big_dict) / cir_c_den_den(ds_obj, x, y)

def calc_cir_b(ds_obj, x, y, big_dict={}):
    return cir_nom(ds_obj, x, y, big_dict=big_dict) / cir_b_den(ds_obj, x)

def calc_cir_c(ds_obj, x, y, big_dict={}):
    nom = cir_nom(ds_obj, x, y, big_dict=big_dict)
    den = cir_c_den(ds_obj, x, y, big_dict=big_dict)
    
    if den == 0:
        return 0
    else:
        return nom / den

if __name__ == '__main__':
    ds_obj = init_obj_test()