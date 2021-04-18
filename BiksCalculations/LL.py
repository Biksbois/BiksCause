import numpy as np
import pandas as pd
from dataset_object import *

def calc_lambda(n, d):
    return n / d

def calc_n(x, u, ds):
    return ds.calc_n(u, x)

def calc_d(u, ds):
    return ds.calc_d(u)

def one_ll(u, x, ds):
    d = calc_d(u, ds)
    n = calc_n(x, u, ds)
    l = calc_lambda(n, d)
    print(l)
    return (- l) * d + n * np.log(l)

def calc_LL(ds):
    set_x = ds.extract_x()
    ll_score = 0

    print(set_x)
    for x in set_x:
        set_u = ds.extract_u(set_x.copy(), x)
        for u in set_u:
            ll_score += one_ll(u, x, ds)

    return ll_score

def get_LL(ds_obj):
    return calc_LL(ds_obj)

if __name__ == '__main__':
    ds_obj = init_obj_test()
    ll = get_LL()
    print(f"The Log Likelihood is: {ll}")