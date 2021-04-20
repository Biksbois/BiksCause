import pandas as pd
from collections import OrderedDict

class dataset():
    def __init__(self, ds_path, col_name, window_size, head_val = -1):
        if head_val == -1:
            self.data = pd.read_csv(ds_path)
        else:
            self.data = pd.read_csv(ds_path).head(head_val)
        
        self.col_dict = {}
        self.window_size = window_size
        self.col_name = col_name
        self.pot_parent = {}
        
        self.create_dict(col_name)
        # self.identify_pot_parents()
        
    def identify_pot_parents(self):
        for win in self.get_window():
            w = win.tolist()
            if w[-1] not in self.pot_parent:
                self.pot_parent[w[-1]] = []
            
            self.pot_parent[w[-1]].extend(w[0:-1])
            self.pot_parent[w[-1]] = list(OrderedDict.fromkeys(self.pot_parent[w[-1]]))

    def calc_suf(self, x, y):
        return self.calc_nec_suf(x, y , False)

    def calc_nec(self, x, y):
        return self.calc_nec_suf(x, y, True)

    def calc_nec_suf(self, x, y, direction):
        result = 0
        for win in self.get_window(backwards=direction):
            if win[0] == x and y in win[1]:
                result += 1
        
        return result / self.get_col_len()

    def extract_x(self):
        return self.data[self.col_name].unique().tolist()
    
    def extract_u(self, x, cur_x):
        x.remove(cur_x)
        return x
    
    def calc_prob(self, key):
        return self.col_dict[key] / self.get_col_len()
    
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
            if u in w[1]:
                result += 1
        return result
    
    def calc_n(self, u, x):
        result = 0
        for w in self.get_window():
            if u in w[1] and w[0] == x: #x in w_list and w_listx.index(x) > w_list.index(u):
                result += 1
        return result
    
    def get_col_len(self):
        return len(self.data[self.col_name])
    
    def calc_min(self, i, window_size):
        return i-(window_size)
    
    def get_window(self, backwards=True):
        for i in range(self.window_size, self.get_col_len()):
            if backwards:
                yield self.data[self.col_name][i], self.data[self.col_name][self.calc_min(i, self.window_size):i].tolist()
            else:
                yield self.data[self.col_name][self.calc_min(i, self.window_size)], self.data[self.col_name][self.calc_min(i, self.window_size)+1:i+1].tolist()

def init_obj_weather_main():
    window_size = 7
    col_name = 'weather_main'
    ds_path = "input_csv\Metro_Interstate_Traffic_Volume.csv"

    return dataset(ds_path, col_name, window_size)

def init_obj_test(head_val = -1):
    window_size = 3
    col_name = 'label'
    ds_path = "data.csv"
    # ds_path = "BiksCalculations\data.csv"

    return dataset(ds_path, col_name, window_size, head_val = head_val)

if __name__ == '__main__':
    obj = init_obj_test()
    
    print(obj.get_col_len())