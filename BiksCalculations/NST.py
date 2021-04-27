from BiksCalculations.dataset_object import *

def calc_den(x, y, alpha_val):
    return (x ** alpha_val) * y

def nst_rhs(ds_obj, alpha_val, lambda_val, x, y, big_dict={}):
    suf = ds_obj.calc_suf(x, y, big_dict=big_dict)
    den = calc_den(ds_obj.calc_effect_prob(x), ds_obj.calc_cause_prob(y), alpha_val)
    
    if suf == 0:
        return 0
    else:
        return (suf / den) ** (lambda_val - 1) 

def nst_lhs(ds_obj, alpha_val, lambda_val, x, y,big_dict={}):
    nes = ds_obj.calc_nec(x, y, big_dict=big_dict)
    den = calc_den(ds_obj.calc_cause_prob(y), ds_obj.calc_effect_prob(x), alpha_val)

    if nes == 0:
        return 0
    else:
        return (nes / den) ** (lambda_val)

def get_nst(ds_obj, alpha_val, lambda_val, x, y, nec_dict={}, suf_dict={}):
    return nst_lhs(ds_obj, alpha_val, lambda_val, x, y, big_dict=nec_dict) * nst_rhs(ds_obj, alpha_val, lambda_val, x, y, big_dict=suf_dict)

if __name__ == '__main__':
    alpha_val = 0.66
    lambda_val = 0.5
    x = 'x'
    y = 'y'
    
    ds_obj = init_obj_test()

    print(f"The NST score for {x} and {y} is: {get_nst(ds_obj, alpha_val, lambda_val, x, y)}")