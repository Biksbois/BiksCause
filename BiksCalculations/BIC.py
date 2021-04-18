from LL import get_LL
from dataset_object import *
import numpy as np

def calc_ln(ds_obj):
    return np.log(ds_obj.get_col_len())

def calc_sum(ds_obj):
    result = 0
    set_x = ds_obj.extract_x()
    
    for x in set_x:
        set_u = ds_obj.extract_u(set_x.copy(), x)
        result += 2**len(set_u)
    
    return result

def calc_BIC(ll, ds_obj):
    ln = calc_ln(ds_obj)
    sum_u = calc_sum(ds_obj)
    bic = ll - (ln * sum_u)
    
    return bic, ln, sum_u

if __name__ == '__main__':
    ds_obj = init_obj_test()
    ll = get_LL(ds_obj)
    bic, ln, sum_u = calc_BIC(ll, ds_obj)
    
    print(f"The ln(T) score is: {ln}")
    print(f"The sum u score is: {sum_u}")
    print(f"The LL score is: {ll}")
    print(f"The BIC score is: {bic}")