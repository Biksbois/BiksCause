from  dataset_object import *
from CIR import *
from NST import *

if __name__ == '__main__':
    ds_obj = init_obj_test()
    decimals = 4
    x = 'x'
    y = 'y'
    z = 'z'
    alpha_val = 0.66
    lambda_val = 0.5
    
    print(f"P(x)={round(ds_obj.calc_prob(x), decimals)}")
    print(f"P(y)={round(ds_obj.calc_prob(y), decimals)}")
    print(f"P(z)={round(ds_obj.calc_prob(z), decimals)}")
    print(f"w={ds_obj.window_size}")
    print(f"T={ds_obj.get_col_len()}")
    print(f"n={ds_obj.get_col_len()}")
    print(f"P^w(y <-- x)={round(ds_obj.calc_nec(x, y), decimals)}")
    print(f"P^w(y --> x)={round(ds_obj.calc_suf(x, y), decimals)}")
    print(f"P^w(y|x)={round(ds_obj.calc_nec(x, y)/ds_obj.calc_prob(x),decimals)}")
    print(f"P^w(x|y)={round(ds_obj.calc_suf(x, y)/ds_obj.calc_prob(y),decimals)}")
    print(f"NST={round(get_nst(ds_obj, alpha_val, lambda_val, x, y), decimals)}")
    print(f"cir nom={cir_nom(ds_obj, x, y)}")
    print(f"cir c den={cir_c_den(ds_obj, x, y)}")
    print(f"cir c={round(calc_cir_c(ds_obj, x, y), decimals)}")
    print(f"cir b={round(calc_cir_b(ds_obj, x, y), decimals)}")



