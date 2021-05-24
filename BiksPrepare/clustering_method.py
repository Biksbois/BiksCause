from copy import deepcopy
import jenkspy as jpy
import numpy as np
from numpy.lib.shape_base import split
import pandas as pd

def optimize_gvf_score():
    pass

# To calculate the goodness of variance (GVF), the first element which is needed, is the groups
# the data is split up in. Therefore we extract an array for each cluster, to compare them. 
# The parameters which are included, is the dataframe df which contains the clusters, and the
# col_name which is a string with the name of the column containing the data.
def create_cl_arrays(df, col_name, cl_col_name):
    df_arr = []
    values = np.asarray(df[cl_col_name].drop_duplicates().values)
    for v in values:
        df_arr.append(np.asarray(df[col_name].loc[df[cl_col_name] == v].values))
    return df_arr

# The method takes two arrays, an array over all the data ds_arr, and an array of the individual clusters cl_arr.
# The sum of squared deviations for array mean (sdam) is then calculated with the formula taking
# the mean of all the data and then minus it with each value in the ds_arr, and the powered by two.
# The next part is finding the sum of squared deviations for class means (sdcm), where the standard deviation is 
# found for each cluster.
def calc_gvf(ds_arr, cl_arr):
    sdam = np.sum((ds_arr - ds_arr.mean()) ** 2)
    sdcm = sum([np.sum((cl - cl.mean()) ** 2) for cl in cl_arr])
    gvf = (sdam - sdcm) / sdam
    return gvf

def create_labels(cl_label_name, cl_num):
    labels = []
    for i in range(cl_num):
        labels.append(cl_label_name + "_" + str(i))
    return labels

def apply_jenks(df, col_name, cl_label_name, cl_num):
    breaks = jpy.jenks_breaks(df[col_name], nb_class=cl_num)
    if len(set(breaks)) == cl_num:
        cl_num -= 1
    return pd.cut(df[col_name],
                        bins=breaks,
                        labels=create_labels(cl_label_name, cl_num),
                        include_lowest=True, duplicates='drop')

def get_jenks(df, cl_col_name, cl_label_name, col_name, min_gvf = 0.9):
    gvf_score = 0
    nclasses = 2  

    # df[cl_col_name] = apply_jenks(df, col_name, 2)
    # ds_arr = np.asarray(df[col_name])
    # cl_arrs = create_cl_arrays(df, col_name)
    # print(len(cl_arrs))
    # gvf_score = calc_gvf(ds_arr, cl_arrs)
    # print(gvf_score)
    while gvf_score < 0.9 and nclasses < len(df[col_name].unique().tolist()):
        try:
            df[cl_col_name] = apply_jenks(df, col_name, cl_label_name, nclasses)
            ds_arr = np.asarray(df[col_name])
            cl_arrs = create_cl_arrays(df, col_name, cl_col_name)
            # print(cl_arrs)
            # print(ds_arr)
            gvf_score = calc_gvf(ds_arr, cl_arrs)
        except:
            pass
        nclasses += 1 
    return df       

def get_specific_jenks(df, cl_col_name, cl_label_name, col_name, nclasses):
    try:
        df[cl_col_name] = apply_jenks(df, col_name, cl_label_name, nclasses)
    except:
        print('Error in the amount of clusters specified')
    return df


# def check_length(df, col_name, min_size = 2):
#     if df.groupby([col_name]).sum() > min_size:
#         return true
#     else:
#         return false

def check_difference(df, col_name):
    return len(df[col_name].unique().tolist()) == 1 or len(df[col_name].unique().tolist()) == 2

def add_to_clust(df, cl_col_name, cl_label_name, col_name, label_num = 1):
    df[cl_col_name] = pd.qcut(df[col_name], q=1, labels=create_labels(cl_label_name, label_num))
    return df

def check_df(df, cl_col_name, cl_label_name, col_name):
    if check_difference(df, col_name):
        df = add_to_clust(df, cl_col_name, cl_label_name, col_name)
    return df

def create_specific_cluster(df, path, col_name, cl_col_name, cl_label_name, cluster_amount):
    jdf = get_specific_jenks(df, cl_col_name, cl_label_name, col_name, cluster_amount)
    jdf.to_csv(path)

def split_arr_arbitary(df_arr, cl_arr, full_arr, clusters, min_score = 0.9):
    prev = ''
    gvf = 0
    if clusters-1 != 0:
        for index in range(len(df_arr)):
            if not df_arr[index] == prev and len(df_arr[:index]) != 0:
                cl_arr[clusters-1] = df_arr[:index]
                t_arr = split_arr_arbitary(df_arr[index:], cl_arr, full_arr, clusters-1)
                if t_arr[1] > min_score:
                    return t_arr
            prev = df_arr[index]
    else: 
        cl_arr[clusters-1] = df_arr
        gvf = calc_gvf(full_arr, cl_arr)
        if min_score < gvf:
            return cl_arr, gvf
    return 0, 0
    
def itterate_array(df_arr, n_clusters, min_score = 0.9):
    gvf = 0
    df_obj = ()
    cl_arr = [0] * n_clusters
    full_arr = deepcopy(df_arr)
    while len(list(set(df_arr))) >= n_clusters and gvf < min_score:
        df_arr = deepcopy(df_arr)
        cl_arr = deepcopy([0] * n_clusters)
        full_arr = deepcopy(df_arr)
        df_obj = split_arr_arbitary(df_arr, cl_arr, full_arr, n_clusters, min_score)
        gvf = df_obj[1]
        n_clusters += 1
    return df_obj[0], n_clusters


def attach_labels(cl_arr,labels):
    cl_arr = list(reversed(cl_arr))
    cl_dict = {}
    for ind in range(len(cl_arr)):
        cl_dict[labels[ind]] = cl_arr[ind]
    return cl_dict

def add_values_to_df(df,label_dict, col_name, cl_col_name):
    for key in label_dict:
        for value in label_dict[key]:
            df.loc[df[col_name] == value, cl_col_name] = key
    return df
    
def add_clusters(df, cl_tupple, col_name, cl_col_name, cl_label_name):
    labels = create_labels(cl_label_name,cl_tupple[1])
    label_dict = attach_labels(cl_tupple[0],labels)
    return add_values_to_df(df, label_dict, col_name, cl_col_name)

def improved_jenks(df, path, col_name, cl_col_name, cl_label_name, cl_num):
    df_arr = np.sort(np.asarray(df[col_name]))
    cl_tupple = itterate_array(df_arr, cl_num)
    jdf = add_clusters(df, cl_tupple, col_name, cl_col_name, cl_label_name)
    jdf.to_csv(path)

def create_cluster(df, path, col_name, cl_col_name, cl_label_name, cl_num = 2):
    improved_jenks(df, path, col_name, cl_col_name, cl_label_name, cl_num)

    # df = check_df(df, cl_col_name, cl_label_name, col_name)
    # jdf = get_jenks(df, cl_col_name, cl_label_name, col_name)
    # jdf.to_csv(path)

def evaluate_gvf(ds_arr, cl_arr):
    return calc_gvf(ds_arr, cl_arr)

if __name__ == '__main__':
    test_x_cluster = {
        'x': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]
    }

    x_cluster = {
        'x': [2, 43, 50, 43, 46]
    }

    y_cluster = {
        'y': [19, 55, 23, 29, 58, 31, 31]
    }

    z_cluster = {
        'z': [38, 47, 52, 24, 59, 6, 15]
    }

    test_x_df = pd.DataFrame(test_x_cluster)

    ijenks = create_cluster(test_x_df, 'test.csv', 'x', 'cl_test', 'cl', 2)