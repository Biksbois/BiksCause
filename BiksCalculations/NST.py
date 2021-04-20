from dataset_object import *

def calc_den(x, y, alpha_val):
    return (x ** alpha_val) * y

def nst_rhs(ds_obj, alpha_val, lambda_val, x, y):
    suf = ds_obj.calc_suf(x, y)
    den = calc_den(ds_obj.calc_prob(x), ds_obj.calc_prob(y), alpha_val)
    
    return (suf / den) ** (lambda_val - 1) 

def nst_lhs(ds_obj, alpha_val, lambda_val, x, y):
    nes = ds_obj.calc_nec(x, y)
    den = calc_den(ds_obj.calc_prob(y), ds_obj.calc_prob(x), alpha_val)

    return (nes / den) ** (lambda_val)

def get_nst(ds_obj, alpha_val, lambda_val, x, y):
    return nst_lhs(ds_obj, alpha_val, lambda_val, x, y) * nst_rhs(ds_obj, alpha_val, lambda_val, x, y)

if __name__ == '__main__':
    alpha_val = 0.66
    lambda_val = 0.5
    x = 'x'
    y = 'y'
    
    ds_obj = init_obj_test()

    print(f"The NST score for {x} and {y} is: {get_nst(ds_obj, alpha_val, lambda_val, x, y)}")