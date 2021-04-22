from dataset_object import *

def cir_nom(ds_obj, x, y):
    n = ds_obj.calc_n(y, x)
    d = ds_obj.calc_d(y)
    return n / d

def cir_b_den(ds_obj, x):
    return ds_obj.calc_effect_prob(x)

def cir_c_den_nom(ds_obj, x, y):
    return ds_obj.effect_dict[x] - ds_obj.calc_n(y, x)

def cir_c_den_den(ds_obj, x, y):
    return ds_obj.get_col_len() - ds_obj.calc_d(y)

def cir_c_den(ds_obj, x, y):
    return cir_c_den_nom(ds_obj, x, y) / cir_c_den_den(ds_obj, x, y)

def calc_cir_b(ds_obj, x, y):
    return cir_nom(ds_obj, x, y) / cir_b_den(ds_obj, x)

def calc_cir_c(ds_obj, x, y):
    nom = cir_nom(ds_obj, x, y)
    den = cir_c_den(ds_obj, x, y)
    
    if den == 0:
        return 0
    else:
        return nom / den

if __name__ == '__main__':
    ds_obj = init_obj_test()
    