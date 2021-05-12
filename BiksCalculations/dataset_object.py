import pandas as pd
import datetime
import sys
from collections import OrderedDict
from BiksCalculations.time_conversion import *

class dataset():
    def __init__(self, ds_path, cause_column, effect_column, window_size, window_method,time_column, window_multiple_method, head_val = -1, hardcoded_cir_m=None):
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
        self.hardcoded_cir_m = hardcoded_cir_m
        
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

    def get_n(self, x, y, big_dict=None):
        if not big_dict == None and x in big_dict and y in big_dict[x]:
            return big_dict[x][y]
        elif not big_dict == None:
            return 0
        else:
            return self.calc_n(y, x)

    def get_n_cir_m(self, x, key, big_dict=None):
        if isinstance(key, list):
            key = tuple(key)
        
        if not big_dict == None and x in big_dict and key in big_dict[x]:
            return big_dict[x][key]
        
        if not big_dict == None:
            # print(f"get N.\n\nx = {x} \nkey = {key}\n----\n\n")
            return 0
        print("ERROR in get N")
        return 0
    
    def get_d_cir_m(self, x, key, d_dict=None):
        if isinstance(key, list):
            key = tuple(key)
        
        if not d_dict == None:
            if key in d_dict:
                return d_dict[key]
        
        if not d_dict == None:
            # print(f"get D.\n\nkey = {key}\n----\n\n")
            return 0
        print("ERROR in get D")
        return 0

    def get_d(self, y, d_dict=None):
        if not d_dict == None and y in d_dict:
            return d_dict[y]
        elif not d_dict == None:
            return 0
        else:
            return self.calc_d(y)

    def calc_suf(self, x, y, suf_dict=None):
        if not suf_dict == None and x in suf_dict and y in suf_dict[x]:
            return suf_dict[x][y] / self.get_col_len() 
        elif not suf_dict == None:
            return 0     
        return self.calc_nec_suf(x, y , False)

    def calc_nec(self, x, y, nec_dict=None):
        if not nec_dict == None and x in nec_dict and y in nec_dict[x]:
            return nec_dict[x][y] / self.get_col_len()
        elif not nec_dict == None: 
            return 0
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

def start_end_method(data, i, cause_column, effect_column, backwards, window_size, time_column):
    # return default_window_method(data, i, cause_column, effect_column, backwards, window_size, time_column, start_end_condition_one, start_end_condition_two, start_end_min_time, start_end_current_time)
    pass #TODO: Implement this

def start_end_multiple_method(data, i, columns, backwards, window_size, time_column):
    # return default_multiple_window_method(data, i, columns, backwards, window_size, time_column, start_end_condition_one, start_end_condition_two, start_end_min_time, start_end_current_time)
    pass #TODO: Implement this


def start_end_condition_one(current_index, data, time_column, min_time):
    # return current_index >= 0 and data[time_column][current_index] >= min_time
    pass #TODO: Implement this


def start_end_condition_two(current_index, col_len, translate_date, time_column, data, current_time):
    # return current_index < col_len and data[time_column][current_index] <= current_time
    pass #TODO: Implement this


def start_end_min_time(current_time, window_size):
    # return current_time - window_size
    pass #TODO: Implement this

def start_end_current_time(data, time_column, i):
    # return data[time_column][i]
    pass #TODO: Implement this

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
        effect = [str(data[c][i]) for c in colums]
        current_index = i - 1
        
        while window_condition_one(current_index, data, time_column, min_time):
            cause.extend([str(data[c][current_index]) for c in colums])
            current_index -= 1
    else:
        effect = [str(data[c][i-window_size]) for c in colums]
        current_index = i - window_size + 1
        
        while window_condition_two(current_index, col_len, translate_date, time_column, data, current_time):
            cause.extend([str(data[c][current_index]) for c in colums])
            
            current_index += 1
    
    return effect, cause

def init_obj_test(cause_column='label', effect_column='label', time_column='time', head_val = -1, ds_path = ''):
    window_size = 3
    if ds_path == '':
        ds_path = "BiksCalculations/csv/data.csv"

    # print(f"---\nA dataset object has been opened in the following path:\n  {ds_path}\n---", flush=True)
    
    return dataset(ds_path, cause_column, effect_column, window_size,number_method, time_column, number_multiple_method, head_val = head_val)

def init_obj_test_trafic(hardcoded_cir_m=None, cause_column='weather_description', effect_column='weather_description', time_column='date_time', head_val = -1, windows_size = 3, ds_path=''):
    window_size = windows_size
    if ds_path == '':   
        ds_path = "input_csv\Metro_Interstate_Traffic_Volume.csv"

    print(f"---\nA dataset object has been opened in the following path:\n  {ds_path}\n---", flush=True)
    
    return dataset(ds_path, cause_column, effect_column , window_size,date_method, time_column, date_multiple_method, head_val = head_val, hardcoded_cir_m=hardcoded_cir_m)

def init_obj_test_medical(cause_column='deathdate', effect_column='race', time_column=('start', 'end'), head_val = -1, windows_size = 3, ds_path=''):
    window_size = windows_size
    if ds_path == '':   
        ds_path = "output_csv\careplans.csv"

    print(f"---\nA dataset object has been opened in the following path:\n  {ds_path}\n---", flush=True)
    
    return dataset(ds_path, cause_column, effect_column, window_size,start_end_method, time_column, start_end_multiple_method, head_val = head_val)

