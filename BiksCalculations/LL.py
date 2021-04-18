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
    # print(f"d = {d}, n = {n}, l = {l}")
    return (- l) * d + n * np.log(l)

def calc_LL(ds):
    set_x = ds.extract_x()
    return ll_with_set(ds, set_x)

def calc_ll_temp(set_u, x, ds):
    ll_temp = 0
    for u in set_u:
        ll_temp += one_ll(u, x, ds)
    return ll_temp

def ll_with_set(ds, set):
    ll_score = 0
    print(set_x)
    for x in set_x:
        set_u = ds.extract_u(set_x.copy(), x)
        ll_temp = calc_ll_temp(set_u, x, ds)
        ll_score += ll_temp
        # print(f"score: {ll_temp}, event: {x}, parents: {set_u}") 

    return ll_score

def ll_with_two_set(ds, set_x, set_u):
    ll_score = 0
    print(set_x)
    for x in set_x:
        ll_temp = calc_ll_temp(set_u, x, ds)
        ll_score += ll_temp
        # print(f"score: {ll_temp}, event: {x}, parents: {set_u}") 
    return ll_score

def get_LL(ds_obj):
    return calc_LL(ds_obj)

if __name__ == '__main__':
    ds_obj = init_obj_test()
    ll = get_LL(ds_obj)
    
    print(f"The Log Likelihood is: {ll}")