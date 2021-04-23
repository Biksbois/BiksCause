import jenkspy as jpy
import numpy as np
import pandas as pd



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
           gvf_score = calc_gvf(ds_arr, cl_arrs)
       except:
           pass
       nclasses += 1 

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
    
def create_cluster(df, path, col_name, cl_col_name, cl_label_name):
    df = check_df(df, cl_col_name, cl_label_name, col_name)
    jdf = get_jenks(df, cl_col_name, cl_label_name, col_name)
    jdf.to_csv(path)

if __name__ == '__main__':
    sales = {
        'Total': [1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 5, 5, 5, 5 ,5, 6, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 10, 10, 10, 10, 10, 10, 10, 10, 11, 11, 11, 11, 11, 11, 11, 11, 12, 12, 12, 12, 12, 12, 26, 26, 26 , 26, 26, 26, 70, 70, 70, 70, 70]
    }
    df = pd.DataFrame(sales)
    create_cluster(df, 'test.csv', 'Total', 'cluster', 'cl')
