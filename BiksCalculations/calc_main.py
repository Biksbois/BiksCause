from BiksCalculations.CIR import *
from BiksCalculations.NST import *
from BiksCalculations.dataset_object import *

def calculate(x, y, ds_obj, matrixes, alpha_val = 0.66, lambda_val = 0.5):
    nst = get_nst(ds_obj, alpha_val, lambda_val, x, y)
    cir_c = calc_cir_c(ds_obj, x, y)
    cir_b = calc_cir_b(ds_obj, x, y)
    
    matrixes['nst'].xs(x)[y] = round(nst, 2)
    matrixes['cir_c'].xs(x)[y] = round(cir_c, 2)
    matrixes['cir_b'].xs(x)[y] = round(cir_b, 2)

def extract_values(colum_list, colum_dict):
    vals_to_check = []
    for key in colum_list:
        vals_to_check.extend(colum_dict[key].keys())
    return vals_to_check

def create_datafram_matric(distinct_values, save_index):
    test_data = [["" for i in range(len(distinct_values))] for i in range(len(distinct_values))]
    data_matrix = pd.DataFrame(test_data, columns = distinct_values, index=distinct_values)
    return data_matrix

def create_matix_path(s, base_path):
    return f'{base_path}/{s}_matrix.csv'
    # return f'BiksCalculations/results/{s}_matrix.csv'

def init_matrixes(scores, distinct_values, base_path):
    matrix_dict = {}
    for s in scores:
        save_path = create_matix_path(s, base_path)
        matrix_dict[s] = create_datafram_matric(distinct_values, save_path)
    return matrix_dict

def do_calculations(cause_column, effect_column, base_path, colum_list):
    scores = ['nst', 'cir_c', 'cir_b']

    print("The differet scores will now be calculated in the following order:")
    for s in scores:
        print(f"    - {s}")

    ds_obj = init_obj_test(cause_column=cause_column, effect_column=effect_column)
    
    colum_dict = {}
    
    for c in colum_list:
        colum_dict[c] = ds_obj.create_dict(c)
    
    distinct_values = extract_values(colum_list, colum_dict)
    
    matrixes = init_matrixes(scores, distinct_values, base_path)
    
    for cause in colum_list:
        ds_obj.cause_dict = colum_dict[cause]
        ds_obj.cause_column = cause
        
        for effect in colum_list:
            ds_obj.effect_dict = colum_dict[effect]
            
            ds_obj.effect_column = effect
            
            for c in colum_dict[cause]:
                for e in colum_dict[effect]:
                    calculate(e, c, ds_obj, matrixes)
    
    for s in scores:
        save_path = create_matix_path(s, base_path)
        matrixes[s].to_csv(save_path, index=True, header=True)