import jenkspy as jpy
import numpy as np
import pandas as pd

cl_col_name = 'Clusters'

def create_cl_arrays(df, col_name):
    df_arr = []
    values = np.asarray(df[cl_col_name].drop_duplicates().values)
    for v in values:
        df_arr.append(np.asarray(df[col_name].loc[df[cl_col_name] == v].values))
    return df_arr

def calc_gvf(ds_arr, cl_arr):
    sdam = np.sum((ds_arr - ds_arr.mean()) ** 2)
    sdcm = sum([np.sum((cl - cl.mean()) ** 2) for cl in cl_arr])
    gvf = (sdam - sdcm) / sdam
    return gvf

def create_labels(cl_num):
    labels = []
    for i in range(cl_num):
        labels.append("cl_" + str(i))
    return labels

def apply_jenks(df, col_name, cl_num):
    breaks = jpy.jenks_breaks(df[col_name], nb_class=cl_num)
    return pd.cut(df[col_name],
                        bins=breaks,
                        labels=create_labels(cl_num),
                        include_lowest=True)

def get_jenks(df, col_name, min_gvf = 0.9):
    gvf_score = 0
    nclasses = 2    

    while gvf_score < min_gvf:
        try:
            df[cl_col_name] = apply_jenks(df, col_name, nclasses)
            ds_arr = np.asarray(df[col_name])
            cl_arrs = create_cl_arrays(df, col_name)
            gvf_score = calc_gvf(ds_arr, cl_arrs)
        except:
            print("Duplicate error.")
        nclasses += 1 

    return df       

def create_cluster(ds, col_name):
    df = pd.DataFrame(ds)
    return get_jenks(df, col_name)

if __name__ == '__main__':
    sales = {
        'Total': [1, 5, 9, 10, 15, 16, 26, 28]
    }
    df = create_cluster(sales, 'Total')
    print(df)