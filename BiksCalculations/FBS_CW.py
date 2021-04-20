from dataset_object import *
from BIC import calc_BIC
from LL import ll_with_two_set

def forward_run(ds_obj, x, set_z):
    return 0

def add_to_list(li, x):
    return li.extend(x)

def forward_search(ds_obj, x):
    set_u = []
    set_z = ds_obj.pot_parent[x]
    score = - 2 ** 10
    previous_score = score
    set_x = [x]
    
    print(f"For event '{x}', the potential parents are {set_z}")
    
    while score == previous_score:
        for z in set_z:
            if z not in set_u:
                # set_u.append(z)
                ll = ll_with_two_set(ds_obj, set_x, add_to_list(set_u.copy(), z))
                
                if ll > score:
                    set_u.append(z)
                    score = ll
                    previous_score = score
                
                print(f"LL = {ll}, set_x = {set_x}, set_u = {set_u}")

def backward_search(ds_obj):
    pass

if __name__ == '__main__':
    ds_obj = init_obj_test()
    x = 'x'
    forward_search(ds_obj, x)
    backward_search(ds_obj)