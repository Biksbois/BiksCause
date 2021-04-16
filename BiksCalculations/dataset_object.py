import pandas as pd

class dataset():
    def __init__(self, ds_path, col_name, window_size):
        self.data = pd.read_csv(ds_path)
        self.col_dict = {}
        self.window_size = window_size
        self.col_name = col_name
        
        self.create_dict(col_name)

    def extract_x(self):
        return self.data[self.col_name].unique().tolist()
    
    def extract_u(self, x, cur_x):
        x.remove(cur_x)
        return x
    
    def count_occurrences(self, col_name):
        return self.data[col_name].value_counts()
    
    def create_dict(self, col_name):
        values = self.count_occurrences(col_name)
        keys = values.index.tolist()
        
        self.keyval_to_dict(keys, values)
    
    def keyval_to_dict(self, key, values):
        for i in range(len(key)):
            self.col_dict[key[i]] = values[i]
    
    def calc_d(self, u):
        result = 0
        for w in self.get_window():
            if u in w.tolist():
                result += 1
        return result
    
    def calc_n(self, u, x):
        result = 0
        for w in self.get_window():
            w_list = w.tolist()
            if u in w_list and x in w_list and w_list.index(x) > w_list.index(u):
                result += 1
        return result
    
    def get_col_len(self):
        return len(self.data[self.col_name]) + 1
    
    def calc_min(self, i):
        return i-self.window_size
    
    def get_window(self):
        for i in range(self.window_size-1, self.get_col_len()):
            yield self.data[self.col_name][self.calc_min(i):i]

def init_obj_weather_main():
    window_size = 7
    col_name = 'weather_main'
    ds_path = "input_csv\Metro_Interstate_Traffic_Volume.csv"

    return dataset(ds_path, col_name, window_size)

def init_obj_test():
    window_size = 3
    col_name = 'label'
    ds_path = "BiksCalculations\data.csv"

    return dataset(ds_path, col_name, window_size)