from CIR import *
from NST import *
from dataset_object import *

alpha_val = 0.66
lambda_val = 0.5

def calculate(x, y, ds_obj):
    # x = e
    # y = c
    
    nst = get_nst(ds_obj, alpha_val, lambda_val, x, y)
    cir_c = calc_cir_c(ds_obj, x, y)
    cir_b = calc_cir_b(ds_obj, x, y)
    
    print(f"\n---\nLooking at:\n  effect '{x}' colum '{ds_obj.effect_column}'\n  cause '{y}',column '{ds_obj.cause_column}'\n  The values are as following:\n")
    print(f"    - NST   = {nst}")
    print(f"    - CIR_c = {cir_c}")
    print(f"    - CIR_b = {cir_b}")
    print('---')

if __name__ == '__main__':
    cause_column = 'label'
    effect_column = 'label'

    ds_obj = init_obj_test(cause_column=cause_column, effect_column=effect_column)
    
    colum_list = ['label', 'test','dur_cluster']
    colum_dict = {}
    

    
    for c in colum_list:
        colum_dict[c] = ds_obj.create_dict(c)
    
    # effect = ''
    # cause = ''
    
    # ds_obj.cause_dict = colum_dict['dur_cluster']
    # ds_obj.effect_dict = colum_dict['dur_cluster']
    # ds_obj.cause_column = 'dur_cluster'
    # ds_obj.effect_column = 'dur_cluster'
    # e = 'c3'
    # c = 'c2'
    
    # calculate(e, c, ds_obj)
    
    for cause in colum_list:
        ds_obj.cause_dict = colum_dict[cause]
        ds_obj.cause_column = cause
        
        for effect in colum_list:
            ds_obj.effect_dict = colum_dict[effect]
            
            print(ds_obj.cause_dict)
            print(ds_obj.effect_dict)
            
            ds_obj.effect_column = effect
            
            for c in colum_dict[cause]:
                for e in colum_dict[effect]:
                    calculate(e, c, ds_obj)
