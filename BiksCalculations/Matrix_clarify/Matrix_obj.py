import pandas as pd
import os
import re

class result_matrix():
    
    def __init__(self, path, matrix_type = 'unspecified'):
        self.df = pd.read_csv (path)
        self.create_label_mapping(self.df)
        self.matrix_type = matrix_type
        self.matrix_list = []
        self.matrix_sorted_list = []
        self.extract_file_config(path)
        
    def create_label_mapping(self, df):
        self.lookup_dict = {}
        for i, head in enumerate(self.df.columns.values.tolist()):
            self.lookup_dict[head] = i
    
    def get_Value(self,col, idx):
        if self.lookup_dict[idx] != 0:
            return self.df[col][self.lookup_dict[idx]-1]
        return 0
    
    def get_type(self):
        return self. matrix_type
    
    def get_most_causal_pair(self, rank = 1):
        if len(self.matrix_list) == 0:
            self.tolist()
            self.sort_matrix()
        elif len(self.matrix_sorted_list) == 0:
            self.sort_matrix()
        return self.matrix_sorted_list[rank]
    
    def sort_matrix(self):
        self.matrix_sorted_list = [(c,i) for c, i, v in [(k,v,self.get_Value(k,v)) for k,v in self.matrix_list]]

    def tolist(self):
        if len(self.matrix_list) == 0:
            for col in self.df.columns.values.tolist()[1:]:
                for idx in self.df.columns.values.tolist()[1:]:
                    self.matrix_list.append((col,idx))
        return self.matrix_list

    def sum_col(self, col):
        return sum(list(self.df[col]))
    
    def matrix_sum(self):
        return sum([self.sum_col(col) for col in self.df.columns.values.tolist()[1:]])
    
    def extract_file_config(self, file):
        alpha_regex = '_a\d+_'
        lambda_regex = '_l\d+_'
        header_regex = '_h\d+_'
        window_regex = '_w\d+_'
        self.window = re.search(window_regex,file).group().replace('_','').replace('w','')
        self.header = re.search(header_regex,file).group().replace('_','').replace('h','')
        if('cir' not in file):
            self.lamb = int(re.search(lambda_regex,file).group().replace('_','').replace('l',''))/10
            self.alpha = int(re.search(alpha_regex,file).group().replace('_','').replace('a',''))/100
            # return (window, header, lamb, alpha)
        # return(window, header)

def get_csv_files_containing(path, score):
    files = []
    for file in os.listdir(path):
        if file.endswith(".csv") and score in file:
            files.append(file)
    return files

def generate_matrix_sum_csv(matrixes):
    mat_sum = []
    header = ['']
    alpha = [] 
    for matrix in matrixes:
        header.append(f"W = {matrix.window}_L = {matrix.lamb}")
        alpha.append(matrix.alpha)
    alp = sorted(list(set(alpha)))
    test_data = [['' for i in range(len(list(set(header))))]for i in range(len(alp))]
    data_matrix = pd.DataFrame(test_data, columns = list(set(header)), index=alp)
    for matrix in matrixes:
        data_matrix.xs(matrix.alpha)[f"W = {matrix.window}_L = {matrix.lamb}"] = matrix.matrix_sum()    
    
    for a in alpha:
        data_matrix.xs(a)[''] = a
    
    data_matrix.to_csv('BiksCalculations\Sum_result\\first.csv',index=False)

def plot_matrixes():
    import matplotlib.pyplot as plt
    import numpy as np
    # Get the data (csv file is hosted on the web)
    url = 'BiksCalculations\Sum_result\\first.csv'
    df = pd.read_csv(url, index_col = 0)
    df.plot()
    plt.show()
    



path = 'BiksCalculations\\results'
matrixs_lst = []
files = get_csv_files_containing(path, 'nst')
for file in files:
    matrixs_lst.append(result_matrix(path+'\\'+file))
generate_matrix_sum_csv(matrixs_lst)
plot_matrixes()
# rs.tolist()
# rs.sort_matrix()
# print(rs.matrix_sum())
#print(rs.matrix_sorted_list[:100])