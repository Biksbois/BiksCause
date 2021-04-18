from dataset_object import *
from BIC import calc_BIC
from LL import ll_with_two_set

def forward_run(ds_obj, x, set_z):
    return 0

def forward_search(ds_obj, x):
    set_u = []
    set_z = ds_obj.pot_parent[x]
    score = forward_run(ds_obj, x, set_z)
    set_x = [x]
    
    print(f"For event '{x}', the potential parents are {set_z}")
    
    # while True:
    for z in set_z:
        if z not in set_u:
            set_u.append(z)
            ll = ll_with_two_set(ds_obj, set_x, set_u)
            print(f"LL = {ll}, set_x = {set_x}, set_u = {set_u}")

def backward_search(ds_obj):
    pass

if __name__ == '__main__':
    ds_obj = init_obj_test()
    
    forward_search(ds_obj, 'x')
    backward_search(ds_obj)