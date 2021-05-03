import pandas as pd

class result_matrix():
    
    def __init__(self, path, matrix_type = 'unspecified'):
        self.df = pd.read_csv (path)
        self.create_label_mapping(self.df)
        self.matrix_type = matrix_type
        self.matrix_list = []
        self.matrix_sorted_list = []
        print(len(self.matrix_sorted_list))
        
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
        
        
rs = result_matrix('BiksCalculations\\results\\traffic_cir_b_h50000_w6_matrix.csv', 'nst')
rs.tolist()
rs.sort_matrix()
print(rs.matrix_sorted_list[:100])
