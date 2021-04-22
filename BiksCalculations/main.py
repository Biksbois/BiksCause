from CIR import *
from NST import *
from dataset_object import *

if __name__ == '__main__':
    cause_column = 'label'
    effect_column = 'label'

    ds_obj = init_obj_test(cause_column=cause_column, effect_column=effect_column)
    
    x = 'x'
    y = 'y'
    
    alpha_val = 0.66
    lambda_val = 0.5

    nst = get_nst(ds_obj, alpha_val, lambda_val, x, y)
    cir_c = calc_cir_c(ds_obj, x, y)
    cir_b = calc_cir_b(ds_obj, x, y)

    print(f"\n---\nLooking at:\n  effect '{x}' from colum '{effect_column}'\n  and\n  cause '{y}' from column '{cause_column}'\n  The values are as following:\n")
    print(f"    - NST   = {nst}")
    print(f"    - CIR_c = {cir_c}")
    print(f"    - CIR_b = {cir_b}")
    print('---')
