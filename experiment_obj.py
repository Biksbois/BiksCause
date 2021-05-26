from main_paths import *
import os

class exp_obj():
    def __init__(self, alpha_val, lambda_val, window_size, head_val, exp_type, exp_size, support, scores):
        self.alpha_val = alpha_val
        self.lambda_val = lambda_val
        self.window_size = window_size
        self.head_val = head_val
        self.exp_type = exp_type
        self.exp_size = exp_size
        self.nst_keys = []#self.generate_nst_keys()
        self.support = support
        self.scores = scores
        # scores.extend(self.nst_keys)
        
    
    def parse_val(self, val):
        return str(val).replace('0.', '')
    
    def one_nst_key(self, a, l):
        return f"nst_a{self.parse_val(a)}_l{self.parse_val(l)}"
    
    def generate_nst_keys(self):
        scores = []
        for a in self.alpha_val:
            for l in self.lambda_val:
                scores.append(self.one_nst_key(a, l))
        
        return scores

class datatype_obj():
    def __init__(self, hardcoded_cir_m, cluster_col_names, baseline_col_names, cluster_colums, ds_path, time_colum, temp_csv_path, cause_column, effect_column, result_path):
        self.hardcoded_cir_m = hardcoded_cir_m
        self.cluster_col_names = cluster_col_names
        self.baseline_col_names = baseline_col_names
        self.cluster_colums = cluster_colums
        self.ds_path = ds_path
        self.time_colum = time_colum
        self.temp_csv_path = temp_csv_path
        self.cause_column = cause_column
        self.effect_column = effect_column
        self.result_path = result_path
        
    def print_stuff(self):
        print(f"hardcoded_cir_m keys: {self.hardcoded_cir_m.keys()}")
        print(f"cluster_col_names: {self.cluster_col_names}")
        print(f"baseline_col_names: {self.baseline_col_names}")
        print(f"cluster_colums: {self.cluster_colums}")
        print(f"ds_path: {self.ds_path}")
        print(f"time_colum: {self.time_colum}")
        print(f"temp_csv_path: {self.temp_csv_path}")
        print(f"cause_column: {self.cause_column}")
        print(f"effect_column: {self.effect_column}")
        print(f"result_path: {self.result_path}")


def get_traffic_datatype_obj():
    hardcoded_cir_m = {
        'cluster':{
            1:{
                'traffic_volume_0': ['heavy intensity rain_0', 'mist_0', 'moderate rain_0', 'traffic_volume_0', 'traffic_volume_2'],
                'traffic_volume_1': ['mist_0', 'moderate rain_0', 'traffic_volume_1', 'light rain_0'],
                'traffic_volume_2': ['heavy intensity rain_0', 'light rain_0', 'moderate rain_0', 'traffic_volume_0', 'traffic_volume_2']
            },
            5:{
                'traffic_volume_0': ['mist_0', 'traffic_volume_0', 'traffic_volume_1', 'traffic_volume_2'],
                'traffic_volume_1': ['mist_0', 'traffic_volume_0', 'traffic_volume_1', 'traffic_volume_2'],
                'traffic_volume_2': ['mist_0', 'traffic_volume_0', 'traffic_volume_1', 'traffic_volume_2'],
            },
            10:{
                'traffic_volume_0': ['moderate rain_0', 'snow_0', 'traffic_volume_0', 'traffic_volume_1'],
                'traffic_volume_1': ['mist_0', 'traffic_volume_0', 'traffic_volume_1', 'traffic_volume_2'],
                'traffic_volume_2': ['mist_0', 'traffic_volume_0', 'traffic_volume_1', 'traffic_volume_2'],
            }
        },
        'no_cluster':{
            1:{
                'traffic_volume_0': ['heavy intensity rain', 'mist', 'moderate rain', 'traffic_volume_0', 'traffic_volume_2'],
                'traffic_volume_1': ['light rain', 'mist', 'moderate rain', 'traffic_volume_1'],
                'traffic_volume_2': ['heavy intensity rain', 'light rain', 'moderate rain', 'traffic_volume_0', 'traffic_volume_2']
            },
            5:{
                'traffic_volume_0': ['moderate rain', 'snow', 'traffic_volume_0', 'traffic_volume_1', 'traffic_volume_2'],
                'traffic_volume_1': ['mist', 'traffic_volume_0', 'traffic_volume_1', 'traffic_volume_2'],
                'traffic_volume_2': ['mist', 'traffic_volume_0', 'traffic_volume_1', 'traffic_volume_2'],
            },
            10:{
                'traffic_volume_0': ['moderate rain', 'snow', 'traffic_volume_0', 'traffic_volume_1'],
                'traffic_volume_1': ['light intensity drizzle', 'snow', 'traffic_volume_0', 'traffic_volume_1', 'traffic_volume_2'],
                'traffic_volume_2': ['mist', 'traffic_volume_0', 'traffic_volume_1', 'traffic_volume_2'],
            }
        }
        }
    
    trafic_column_list = ['temp_cluster','traffic_volume_cluster']
    
    trafic_cluster_col_names = ['weather_description_cluster'] + trafic_column_list
    trafic_baseline_col_names = ['weather_description'] + trafic_column_list
    
    trafic_cluster_colums = [('traffic_volume', True), ('temp', True), ('clouds_all', True), ('weather_description', False)]
    
    cause_column, effect_column = get_cause_effect_col()
    result_path = f"{get_result_path()}/traffic"
    
    ds_path = [get_large_traffic()]
    time_colum = get_trafic_time()
    temp_csv_path = get_temp_csv_path()
    
    return datatype_obj(hardcoded_cir_m, trafic_cluster_col_names, trafic_baseline_col_names, trafic_cluster_colums, ds_path, time_colum, temp_csv_path, cause_column, effect_column, result_path)

def get_synthetic_datatype_obj():
    hardcoded_cir_m = None
    
    cluster_col_names = ['events_cluster']
    baseline_col_names = ['events']
    
    cluster_colums = [('events', False)]
    
    cause_column = 'events'
    effect_column = 'events'
    
    result_path = f"{get_result_path()}/synthetic"
    
    ds_path = []
    
    base = 'output_csv\generated_data'
    
    for f in os.listdir(base):
        ds_path.append(f"{base}/{f}")
    
    time_colum = 'time_set'
    temp_csv_path = get_temp_csv_path()
    
    return datatype_obj(hardcoded_cir_m, cluster_col_names, baseline_col_names, cluster_colums, ds_path, time_colum, temp_csv_path, cause_column, effect_column, result_path)

def get_air_datatype_obj():
    hardcoded_cir_m = None
    
    col_names = ['PM10_cluster']
    # col_names = ['PM10_cluster', 'TEMP_cluster', 'PRES_cluster', 'DEWP_cluster', 'RAIN_cluster', 'wd_cluster']
    
    cluster_col_names = ['TEMP_cluster_cluster', 'PRES_cluster_cluster', 'DEWP_cluster_cluster', 'WSPM_cluster_cluster'] + col_names
    baseline_col_names = ['TEMP_cluster', 'PRES_cluster', 'DEWP_cluster', 'WSPM_cluster'] + col_names
    
    # cluster_colums = [('PM2.5', True), ('PM10', True), ('TEMP', True), ('PRES', True), ('DEWP', True), ('RAIN', True), ('wd', False), ('WSPM', True)]
    # cluster_colums = [('TEMP_cluster', False), ('PRES_cluster', False), ('DEWP_cluster', False),('RAIN_cluster', False),('WSPM_cluster', False)]
    cluster_colums = [('PM10_cluster', False)]#, ('TEMP_cluster', False)]#, ('PRES_cluster', False), ('DEWP_cluster', False),('RAIN_cluster', False),('WSPM_cluster', False)]
    
    cause_column = 'PM2.5'
    effect_column = 'PM2.5'
    
    result_path = f"{get_result_path()}/air"
    
    ds_path = ['input_csv\PRSA_Data_Dongsi_spring.csv',
            'input_csv\PRSA_Data_Dongsi_summer.csv', 
            'input_csv\PRSA_Data_Dongsi_fall.csv', 
            'input_csv\PRSA_Data_Dongsi_winter.csv']
    
    # ds_path = ['input_csv\PRSA_Data_Dongsi_20130301-20170228.csv']
    
    time_colum = 'time_set'
    temp_csv_path = get_temp_csv_path()
    
    return datatype_obj(hardcoded_cir_m, cluster_col_names, baseline_col_names, cluster_colums, ds_path, time_colum, temp_csv_path, cause_column, effect_column, result_path)


def get_datatype(exp_type):
    if exp_type == 'traffic':
        return get_traffic_datatype_obj()
    elif exp_type == 'synthetic':
        return get_synthetic_datatype_obj()
    elif exp_type == 'air':
        return get_air_datatype_obj()
    else:
        print(f"---\n'{exp_type}' is not a valid experiment to run.\n---")