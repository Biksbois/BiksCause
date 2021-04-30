import jenkspy as jpy
import numpy as np
import pandas as pd

def calc_silhoutte():
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
    test_x_cluster = {
        'x': [2, 43, 50, 43, 46]
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

    x_df = pd.DataFrame(x_cluster)
    y_df = pd.DataFrame(y_cluster)
    z_df = pd.DataFrame(z_cluster)

    x_df['x_cl'] = apply_jenks(x_df, 'x', 'x_cl', 3)
    y_df['y_cl'] = apply_jenks(y_df, 'y', 'y_cl', 3)
    z_df['z_cl'] = apply_jenks(z_df, 'z', 'z_cl', 3)

    x_ds_arr = np.asarray(x_df['x'])
    y_ds_arr = np.asarray(y_df['y'])
    z_ds_arr = np.asarray(z_df['z'])

    x_cl_arr = create_cl_arrays(x_df, 'x', 'x_cl')
    y_cl_arr = create_cl_arrays(y_df, 'y', 'y_cl')
    z_cl_arr = create_cl_arrays(z_df, 'z', 'z_cl')

    x_gvf = calc_gvf(x_ds_arr, x_cl_arr)
    y_gvf = calc_gvf(y_ds_arr, y_cl_arr)
    z_gvf = calc_gvf(z_ds_arr, z_cl_arr)

    print("X_Cluster: \n{} \n{}, the GVF score equals {}.".format(x_df['x'],x_df['x_cl'],x_gvf))
    print("X_Cluster: \n{} \n{}, the GVF score equals {}.".format(y_df['y'],y_df['y_cl'],y_gvf))
    print("X_Cluster: \n{} \n{}, the GVF score equals {}.".format(z_df['z'],z_df['z_cl'],z_gvf))

    test_x_df = pd.DataFrame(test_x_cluster)
    jdf = get_jenks(test_x_df, 'cl_test', 'cl', 'x')
    print("X_Cluster: \n{} \n{}.".format(test_x_df['x'],test_x_df['cl_test']))
    

