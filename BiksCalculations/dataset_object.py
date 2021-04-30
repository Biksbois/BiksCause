import pandas as pd
import datetime
from collections import OrderedDict
from BiksCalculations.time_conversion import *

class dataset():
    def __init__(self, ds_path, cause_column, effect_column, window_size, window_method,time_column, window_multiple_method, head_val = -1):
        if head_val == -1:
            self.data = pd.read_csv(ds_path)
        else:
            self.data = pd.read_csv(ds_path).head(head_val)
        
        self.window_method = window_method
        self.window_multiple_method = window_multiple_method
        self.window_size = window_size
        self.time_column=time_column
        self.cause_column = cause_column
        self.effect_column = effect_column
        self.pot_parent = {}
        self.length = -1
        
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

    def calc_suf(self, x, y, suf_dict=None):
        if not suf_dict == None and x in suf_dict and y in suf_dict[x]:
            return suf_dict[x][y] / self.get_col_len() 
        elif not suf_dict == None:
            suf = self.calc_nec_suf(x, y , False, divide=False)
            
            if not x in suf_dict:
                suf_dict[x] = {}
            
            suf_dict[x][y] = suf
            return suf / self.get_col_len() 
        # print("CALC_SUF")       
        return self.calc_nec_suf(x, y , False)

    def calc_nec(self, x, y, nec_dict=None):
        if not nec_dict == None and x in nec_dict and y in nec_dict[x]:
            return nec_dict[x][y] / self.get_col_len()
        elif not nec_dict == None:
            nec = self.calc_nec_suf(x, y , True, divide=False)
            
            if not x in nec_dict:
                nec_dict[x] = {}
            
            nec_dict[x][y] = nec
            return nec / self.get_col_len() 
        return self.calc_nec_suf(x, y, True)

    def calc_nec_suf(self, x, y, direction, divide = True):
        result = 0
        for win in self.get_window(backwards=direction):
            if win[0] == x and y in win[1]:
                result += 1
        
        if divide:
            return result / self.get_col_len()
        else:
            return result

    def extract_x(self):
        return self.data[self.effect_column].unique().tolist()
    
    def extract_u(self):
        return self.data[self.cause_column].unique().tolist()
    
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
        if self.length == -1:
            self.length = len(self.data[self.effect_column])
        return self.length
    
    def get_window(self, backwards=True):
        for i in range(self.window_size, self.get_col_len()):
            yield self.window_method(self.data, i, self.cause_column, self.effect_column, backwards, self.window_size, self.time_column)

    def get_multiple_window(self, columns, backwards=True):
            for i in range(self.window_size, self.get_col_len()):
                yield self.window_multiple_method(self.data, i, columns, backwards, self.window_size, self.time_column)


def init_obj_weather_main():
    window_size = 7
    col_name = 'weather_main'
    ds_path = "input_csv\Metro_Interstate_Traffic_Volume.csv"

    return dataset(ds_path, col_name, window_size)

# def test_window_method(data, i, cause_column, effect_column, backwards, window_size, time_column):
#     current_time = data[time_column][i]
#     min_time = current_time - window_size
#     effect = ""
#     cause = []
    
#     col_len = len(data[cause_column])
    
#     if backwards:
#         effect = data[effect_column][i]
#         current_index = i - 1
        
#         while current_index >= 0 and data[time_column][current_index] >= min_time:
#             cause.append(data[cause_column][current_index])
#             current_index -= 1
#     else:
#         effect = data[effect_column][i-window_size]
#         current_index = i - window_size + 1
        
#         while current_index < col_len and data[time_column][current_index] <= current_time:
#             cause.append(data[cause_column][current_index])
#             current_index += 1
    
#     return effect, cause

# def date_window_method(data, i, cause_column, effect_column, backwards, window_size, time_column):
#     current_time = translate_date(data[time_column][i])
#     min_time = current_time - datetime.timedelta(hours=window_size) 
#     effect = ""
#     cause = []
    
#     col_len = len(data[cause_column])
    
#     if backwards:
#         effect = data[effect_column][i]
#         current_index = i - 1
        
#         while current_index >= 0 and calc_deltatime(translate_date(data[time_column][current_index]),min_time) <= 0:
#             cause.append(data[cause_column][current_index])
#             current_index -= 1
#     else:
#         effect = data[effect_column][i-window_size]
#         current_index = i - window_size + 1
        
#         while current_index < col_len and calc_deltatime(translate_date(data[time_column][current_index]), current_time) >= 0:
#             cause.append(data[cause_column][current_index])
#             current_index += 1
    
#     return effect, cause

def number_method(data, i, cause_column, effect_column, backwards, window_size, time_column):
    return default_window_method(data, i, cause_column, effect_column, backwards, window_size, time_column, number_condition_one, number_condition_two, number_min_time, number_current_time)

def number_multiple_method(data, i, columns, backwards, window_size, time_column):
    return default_multiple_window_method(data, i, columns, backwards, window_size, time_column, number_condition_one, number_condition_two, number_min_time, number_current_time)

def number_condition_one(current_index, data, time_column, min_time):
    return current_index >= 0 and data[time_column][current_index] >= min_time

def number_condition_two(current_index, col_len, translate_date, time_column, data, current_time):
    return current_index < col_len and data[time_column][current_index] <= current_time

def number_min_time(current_time, window_size):
    return current_time - window_size

def number_current_time(data, time_column, i):
    return data[time_column][i]

def date_method(data, i, cause_column, effect_column, backwards, window_size, time_column):
    return default_window_method(data, i, cause_column, effect_column, backwards, window_size, time_column, date_condition_one, date_condition_two, date_min_time, date_current_time)

def date_multiple_method(data, i, columns, backwards, window_size, time_column):
    return default_multiple_window_method(data, i, columns, backwards, window_size, time_column, date_condition_one, date_condition_two, date_min_time, date_current_time)

def date_condition_one(current_index, data, time_column, min_time):
    return current_index >= 0 and calc_deltatime(translate_date(data[time_column][current_index]),min_time) <= 0

def date_condition_two(current_index, col_len, translate_date, time_column, data, current_time):
    return current_index < col_len and calc_deltatime(translate_date(data[time_column][current_index]), current_time) >= 0

def date_min_time(current_time, window_size):
    return current_time - datetime.timedelta(hours=window_size)

def date_current_time(data, time_column, i):
    return translate_date(data[time_column][i])

def default_window_method(data, i, cause_column, effect_column, backwards, window_size, time_column, window_condition_one, window_condition_two, min_time_method, current_time_method):
    current_time = current_time_method(data, time_column, i)
    min_time = min_time_method(current_time, window_size)
    effect = ""
    cause = []
    
    col_len = len(data[cause_column])
    
    if backwards:
        effect = data[effect_column][i]
        current_index = i - 1
        
        while window_condition_one(current_index, data, time_column, min_time):
            cause.append(data[cause_column][current_index])
            current_index -= 1
    else:
        effect = data[effect_column][i-window_size]
        current_index = i - window_size + 1
        
        while window_condition_two(current_index, col_len, translate_date, time_column, data, current_time):
            cause.append(data[cause_column][current_index])
            current_index += 1
    
    return effect, cause

def default_multiple_window_method(data, i, colums, backwards, window_size, time_column, window_condition_one, window_condition_two, min_time_method, current_time_method):
    current_time = current_time_method(data, time_column, i)
    min_time = min_time_method(current_time, window_size)
    effect = ""
    cause = []
    
    col_len = len(data[colums[0]])
    
    if backwards:
        # effect = data[effect_column][i]
        effect = [str(data[c][i]) for c in colums]
        current_index = i - 1
        
        while window_condition_one(current_index, data, time_column, min_time):
            # cause.append(data[cause_column][current_index])
            cause.extend([str(data[c][current_index]) for c in colums])
            current_index -= 1
    else:
        effect = [str(data[c][i-window_size]) for c in colums]
        # effect = data[effect_column][i-window_size]
        current_index = i - window_size + 1
        
        while window_condition_two(current_index, col_len, translate_date, time_column, data, current_time):
            # cause.append(data[cause_column][current_index])
            cause.extend([str(data[c][current_index]) for c in colums])
            
            current_index += 1
    
    return effect, cause

def init_obj_test(cause_column='label', effect_column='label', time_column='time', head_val = -1, ds_path = ''):
    window_size = 3
    if ds_path == '':
        ds_path = "BiksCalculations/csv/data.csv"

    print(f"---\nA dataset object has been opened in the following path:\n  {ds_path}\n---",flush=True)
    
    return dataset(ds_path, cause_column, effect_column, window_size,number_method, time_column, number_multiple_method, head_val = head_val)

def init_obj_test_trafic(cause_column='weather_description', effect_column='weather_description', time_column='date_time', head_val = -1, windows_size = 3, ds_path=''):
    window_size = windows_size
<<<<<<< HEAD
    if ds_path == '':   
        ds_path = "BiksCalculations/csv/ny_trafic.csv"
=======
    # col_name = 'weather_description'
    # if ds_path == '':   
    ds_path = "input_csv\Metro_Interstate_Traffic_Volume.csv"
>>>>>>> df8e36a2c6a7b24da1c3163c1a173f6f95e4eec3

    print(f"---\nA dataset object has been opened in the following path:\n  {ds_path}\n---",flush=True)

    return dataset(ds_path, cause_column, effect_column , window_size,date_method, time_column, date_multiple_method, head_val = head_val)

if __name__ == '__main__':
    obj = init_obj_test()
    print(obj.get_col_len())