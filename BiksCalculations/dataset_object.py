import pandas as pd
import datetime
from collections import OrderedDict

class dataset():
    def __init__(self, ds_path, cause_column, effect_column, window_size, window_method,time_column, head_val = -1):
        if head_val == -1:
            self.data = pd.read_csv(ds_path)
        else:
            self.data = pd.read_csv(ds_path).head(head_val)
        
        self.window_method = window_method
        self.window_size = window_size
        self.time_column=time_column
        self.cause_column = cause_column
        self.effect_column = effect_column
        self.pot_parent = {}
        
        self.cause_dict = self.create_dict(cause_column)
        self.effect_dict = self.create_dict(effect_column)
        
        # self.create_dict(cause_column, effect_column)
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
    
    def calc_cause_prob(self, key):
        return self.cause_dict[key] / self.get_col_len()

    def calc_effect_prob(self, key):
        return self.effect_dict[key] / self.get_col_len()
    
    def count_occurrences(self, col_name):
        return self.data[col_name].value_counts()
    
    def create_dict(self, col):
        values = self.count_occurrences(col)
        keys = values.index.tolist()
        
        return self.keyval_to_dict(keys, values)
    
    def keyval_to_dict(self, key, values):
        d = {}
        for i in range(len(key)):
            d[key[i]] = values[i]
        return d
    
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
        return len(self.data[self.effect_column])
    
    def get_window(self, backwards=True):
        for i in range(self.window_size, self.get_col_len()):
            yield self.window_method(self.data, i, self.cause_column, self.effect_column, backwards, self.window_size, self.time_column)

def init_obj_weather_main():
    window_size = 7
    col_name = 'weather_main'
    ds_path = "input_csv\Metro_Interstate_Traffic_Volume.csv"

    return dataset(ds_path, col_name, window_size)

def test_window_method(data, i, cause_column, effect_column, backwards, window_size, time_column):
    current_time = data[time_column][i]
    min_time = current_time - window_size
    effect = ""
    cause = []
    
    col_len = len(data[cause_column])
    
    if backwards:
        effect = data[effect_column][i]
        current_index = i - 1
        
        while current_index >= 0 and data[time_column][current_index] >= min_time:
            cause.append(data[cause_column][current_index])
            current_index -= 1
    else:
        effect = data[effect_column][i-window_size]
        current_index = i - window_size + 1
        
        while current_index < col_len and data[time_column][current_index] <= current_time:
            cause.append(data[cause_column][current_index])
            current_index += 1
    
    return effect, cause

def translate_date(date):
    return datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S') # 2012-10-02 09:00:00

def calc_deltatime(t1, t2):
    diff = t2-t1
    days, seconds = diff.days, diff.seconds
    hours = days * 24 + seconds // 3600
    return hours

def date_window_method(data, i, cause_column, effect_column, backwards, window_size, time_column):
    current_time = translate_date(data[time_column][i])
    min_time = current_time - datetime.timedelta(hours=window_size) 
    effect = ""
    cause = []
    
    col_len = len(data[cause_column])
    
    if backwards:
        effect = data[effect_column][i]
        current_index = i - 1
        
        while current_index >= 0 and calc_deltatime(translate_date(data[time_column][current_index]),min_time) <= 0:
            cause.append(data[cause_column][current_index])
            current_index -= 1
    else:
        effect = data[effect_column][i-window_size]
        current_index = i - window_size + 1
        
        while current_index < col_len and calc_deltatime(translate_date(data[time_column][current_index]), current_time) >= 0:
            cause.append(data[cause_column][current_index])
            current_index += 1
    
    return effect, cause


def init_obj_test(cause_column='label', effect_column='label', time_column='time', head_val = -1):
    window_size = 3
    # col_name = 'label'
    ds_path = "data.csv"
    # ds_path = "BiksCalculations\data.csv"

    return dataset(ds_path, cause_column, effect_column, window_size,test_window_method, time_column, head_val = head_val)

def init_obj_test_trafic(cause_column='weather_description', effect_column='weather_description', time_column='date_time', head_val = -1, windows_size = 3):
    window_size = windows_size
    # col_name = 'weather_description'
    ds_path = "ny_trafic.csv"

    return dataset(ds_path, cause_column, effect_column , window_size,date_window_method, time_column, head_val = head_val)

if __name__ == '__main__':
    obj = init_obj_test()
    print(obj.get_col_len())