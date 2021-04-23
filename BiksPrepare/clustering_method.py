import jenkspy as jpy
import numpy as np
import pandas as pd

cl_col_name = 'Clusters'


# To calculate the goodness of variance (GVF), the first element which is needed, is the groups
# the data is split up in. Therefore we extract an array for each cluster, to compare them. 
# The parameters which are included, is the dataframe df which contains the clusters, and the
# col_name which is a string with the name of the column containing the data.
def create_cl_arrays(df, col_name):
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

def create_cluster(ds, path, col_name):
    df = pd.DataFrame(ds)
    jdf = get_jenks(df, col_name)
    jdf.to_csv(path)

if __name__ == '__main__':
    sales = {
        'Total': [1, 5, 9, 10, 15, 16, 26, 28]
    }
    create_cluster(sales,'Total')
