import pandas as pd
import os
import re
import math

class result_matrix():
    
    def __init__(self, path, matrix_type = 'unspecified'):
        self.df = pd.read_csv (path)
        self.create_label_mapping(self.df)
        self.matrix_type = matrix_type
        self.matrix_list = []
        self.matrix_sorted_list = []
        self.interesting_results = []
        self.interesting_sum = []
        self.translated_pairs = []
        self.extract_file_config(path)
        self.score = 0
        self.initialize_lists()
        
        self.event_to_value = {
            "rain":[12.1,14,"rain"],
            "fog":[-7,1.1,"fog"],
            "mist":[7,"mist"],
            "haze":[14,"haze"],
            "snow":[-37.9,-65,"snow"],
            "light_fog":[1.4,"light_fog"],
            "dense_fog":[-8.3,"dense_fog"],
            "heavy_dense_fog":[-12.5,"heavy_dense_fog"],
            "light_rain":[-8.3,"light_rain"],
            "heavy_rain":[-3.4,"heavy_rain"],
            "exstremly_heavy_rain":[-13.5,"exstremly_heavy_rain"],
            "exstremly_heavy_snow":[-67.6,"exstremly_heavy_snow"],
            "hail":[6.8,"hail"],
            "thunderstorm":[-4.18,"thunderstorm"],
            "traffic_volume_2": [4131,7100],
            "traffic_volume_0": [269,1880],
            "traffic_volume_1": [1881,4130]
        }
        self.mapper_no = {
            "sky is clear_0" : "none",
            "mist_0" : self.event_to_value["dense_fog"],
            "broken clouds_0" : "none",
            "light rain_0" : self.event_to_value["light_rain"],
            "broken clouds_1" : "none",
            "moderate rain_0" : self.event_to_value["rain"],
            "overcast clouds_0" : "none",
            "overcast clouds_2" : "none",
            "overcast clouds_1" : "none",
            "scattered clouds_0" : "none",
            "light intensity drizzle_0" : self.event_to_value["light_rain"],
            "haze_0" : self.event_to_value["light_fog"],
            "light rain_1" : self.event_to_value["light_rain"],
            "few clouds_1" : "none",
            "light snow_0" : self.event_to_value["snow"],
            "scattered clouds_2" : "none",
            "scattered clouds_1" : "none",
            "fog_0" :  self.event_to_value["heavy_dense_fog"],
            "overcast clouds_3" : "none",
            "mist_1" : self.event_to_value["dense_fog"],
            "mist_2" : self.event_to_value["dense_fog"],
            "broken clouds_2" : "none",
            "drizzle_0" : self.event_to_value["light_rain"],
            "proximity thunderstorm_0" : self.event_to_value["thunderstorm"],
            "few clouds_0" : "none",
            "scattered clouds_3" : "none",
            "heavy intensity rain_0" : self.event_to_value["heavy_rain"],
            "few clouds_2" : "none",
            "heavy snow_0" : self.event_to_value["exstremly_heavy_snow"],
            "light snow_1" : self.event_to_value["snow"],
            "mist_3" : self.event_to_value["dense_fog"],
            "light snow_2" : self.event_to_value["snow"],
            "overcast clouds_4" : "none",
            "light rain_2" : self.event_to_value["light_rain"],
            "snow_0" : self.event_to_value["snow"],
            "light snow_3" : self.event_to_value["snow"],
            "broken clouds_3" : "none",
            "moderate rain_1" : self.event_to_value["rain"],
            "mist_4" : self.event_to_value["dense_fog"],
            "haze_1" : self.event_to_value["light_fog"],
            "proximity shower rain_0" : self.event_to_value["heavy_rain"],
            "mist_5" : self.event_to_value["dense_fog"],
            "thunderstorm_0" : self.event_to_value["thunderstorm"],
            "light snow_4" : self.event_to_value["snow"],
            "proximity thunderstorm_1" : self.event_to_value["thunderstorm"],
            "heavy snow_1" : self.event_to_value["exstremly_heavy_snow"],
            "thunderstorm with heavy rain_0" : self.event_to_value["thunderstorm"],
            "broken clouds_4" : "none",
            "drizzle_1" : self.event_to_value["light_rain"],
            "heavy intensity drizzle_0" : self.event_to_value["light_rain"],
            "thunderstorm with light rain_0" : self.event_to_value["thunderstorm"],
            "fog_1" : self.event_to_value["heavy_dense_fog"],
            "haze_2" : self.event_to_value["light_fog"],
            "proximity thunderstorm with rain_0" : self.event_to_value["thunderstorm"],
            "heavy snow_3" : self.event_to_value["exstremly_heavy_snow"],
            "mist_6" : self.event_to_value["dense_fog"],
            "heavy snow_2" : self.event_to_value["exstremly_heavy_snow"],
            "thunderstorm with rain_0" : self.event_to_value["thunderstorm"],
            "haze_3" : self.event_to_value["light_fog"],
            "haze_7" : self.event_to_value["light_fog"],
            "proximity thunderstorm_2" : self.event_to_value["thunderstorm"],
            "heavy snow_4" : self.event_to_value["exstremly_heavy_snow"],
            "fog_2" : self.event_to_value["heavy_dense_fog"],
            "smoke_0" : "none",
            "very heavy rain_0" : self.event_to_value["exstremly_heavy_rain"],
            "heavy intensity rain_1" : self.event_to_value["rain"],
            "haze_4" : self.event_to_value["light_fog"],
            "heavy intensity rain_2" : self.event_to_value["rain"],
            "heavy snow_6" : self.event_to_value["exstremly_heavy_snow"],
            "thunderstorm with light drizzle_0" : self.event_to_value["thunderstorm"],
            "proximity thunderstorm with drizzle_0" : self.event_to_value["thunderstorm"],
            "light intensity shower rain_0" : self.event_to_value["light_rain"],
            "snow_1" : self.event_to_value["snow"],
            "haze_8" : self.event_to_value["light_fog"],
            "light shower snow_0" : self.event_to_value["snow"],
            "haze_5" : self.event_to_value["light_fog"],
            "moderate rain_2" : self.event_to_value["rain"],
            "heavy snow_5" : self.event_to_value["exstremly_heavy_snow"],
            "light rain and snow_0" : self.event_to_value["snow"],
            "shower drizzle_0" : self.event_to_value["light_rain"],
            "haze_6" : self.event_to_value["light_fog"],
            "scattered clouds_4" : "none",
            "heavy intensity drizzle_1" : self.event_to_value["rain"],
            "mist_7" : self.event_to_value["dense_fog"],
            "SQUALLS_0" : "none",
            "sleet_0" : "none",
            "thunderstorm with rain_1" : self.event_to_value["thunderstorm"],
            "freezing rain_0" : self.event_to_value["rain"],
            "few clouds_3" : "none",
            "thunderstorm with drizzle_0" : self.event_to_value["thunderstorm"],
            "proximity thunderstorm with rain_1" : self.event_to_value["thunderstorm"],
            "proximity shower rain_1" : self.event_to_value["rain"],
            "heavy intensity rain_3" : self.event_to_value["heavy_rain"],
            "light intensity drizzle_1" : self.event_to_value["light_rain"], 
            "drizzle_2" : self.event_to_value["light_rain"],
            "proximity thunderstorm_3" : self.event_to_value["thunderstorm"],
            "sky is clear_1" : "none",
            "snow_2" : self.event_to_value["snow"],
            "shower snow_0" : self.event_to_value["snow"],
            "light rain_3" : self.event_to_value["light_rain"],
            "temp_6": "none",
            "temp_3": "none",
            "temp_5": "none",
            "temp_2": "none",
            "temp_4": "none",
            "temp_7": "none",
            "temp_1": "none",
            "temp_0": "none",
            "traffic_volume_2": self.event_to_value["traffic_volume_2"],
            "traffic_volume_0": self.event_to_value["traffic_volume_0"],
            "traffic_volume_1": self.event_to_value["traffic_volume_1"]
        }
        self.mapper = {
            "Sky is Clear": "none",
            "sky is clear": "none",
            "mist":  self.event_to_value["dense_fog"],
            "broken clouds":"none",
            "light rain":self.event_to_value["light_rain"],
            "moderate rain":self.event_to_value["rain"],
            "overcast clouds": "none",
            "scattered clouds":"none",
            "light intensity drizzle": self.event_to_value["light_rain"],
            "haze": self.event_to_value["light_fog"],
            "few clouds":"none",
            "light snow":self.event_to_value["snow"],
            "fog":self.event_to_value["heavy_dense_fog"],
            "drizzle":self.event_to_value["light_rain"],
            "proximity thunderstorm":self.event_to_value["thunderstorm"],
            "few clouds":"none",
            "heavy snow":self.event_to_value["exstremly_heavy_snow"],
            "proximity shower rain":self.event_to_value["rain"],
            "thunderstorm":self.event_to_value["light_rain"],
            "proximity thunderstorm":self.event_to_value["thunderstorm"],
            "thunderstorm with heavy rain":self.event_to_value["light_rain"],
            "thunderstorm with light rain":self.event_to_value["light_rain"],
            "haze":self.event_to_value["light_fog"],
            "thunderstorm with rain":self.event_to_value["light_rain"],
            "very heavy rain":self.event_to_value["exstremly_heavy_rain"],
            "heavy intensity rain":self.event_to_value["heavy_rain"],
            "thunderstorm with light drizzle":self.event_to_value["light_rain"],
            "proximity thunderstorm with drizzle":self.event_to_value["light_rain"],
            "light intensity shower rain":self.event_to_value["light_rain"],
            "snow":self.event_to_value["snow"],
            "light shower snow":self.event_to_value["snow"],
            "moderate rain":self.event_to_value["rain"],
            "light rain and snow":self.event_to_value["snow"],
            "shower drizzle":self.event_to_value["light_rain"],
            "heavy intensity drizzle":self.event_to_value["rain"],
            "SQUALLS":"none",
            "sleet":"none",
            "smoke":"none",
            "thunderstorm with rain":self.event_to_value["light_rain"],
            "freezing rain":self.event_to_value["rain"],
            "thunderstorm with drizzle":self.event_to_value["thunderstorm"],
            "proximity thunderstorm with rain":self.event_to_value["light_rain"],
            "shower snow": self.event_to_value["snow"],
            "temp_6":"none",
            "temp_3":"none",
            "temp_5":"none",
            "temp_2":"none",
            "temp_4":"none",
            "temp_7":"none",
            "temp_1":"none",
            "temp_0":"none",
            "traffic_volume_2": self.event_to_value["traffic_volume_2"],
            "traffic_volume_0": self.event_to_value["traffic_volume_0"],
            "traffic_volume_1": self.event_to_value["traffic_volume_1"]
        }
        
    def initialize_lists(self):
        self.tolist()
        self.sort_matrix()
        self.get_interesting_result("traffic")
        self.translate_causal_pairs()
        self.interesting_sum = sum(self.get_list_Value(self.interesting_results))
        
    def extract_file_config(self, file):
        alpha_regex,lambda_regex,header_regex,window_regex = ('_a\d+_','_l\d+_','_h\d+_','_w\d+_')
        self.window = re.search(window_regex,file).group().replace('_','').replace('w','')
        self.header = re.search(header_regex,file).group().replace('_','').replace('h','')
        if('cir' not in file):
            self.lamb = int(re.search(lambda_regex,file).group().replace('_','').replace('l',''))/10
            self.alpha = int(re.search(alpha_regex,file).group().replace('_','').replace('a',''))/100
            
    def create_label_mapping(self, df):
        self.lookup_dict = {}
        for i, head in enumerate(self.df.columns.values.tolist()):
            self.lookup_dict[head] = i
    
    def get_Value(self,pair):
        col,idx = pair
        if self.lookup_dict[idx] != 0 and not math.isnan(float(self.df[col][self.lookup_dict[idx]-1])):
            return self.df[col][self.lookup_dict[idx]-1]
        return 0
    
    def get_list_Value(self,lst):
        return_lst = []
        for pair in lst:
            return_lst.append(self.get_Value(pair))
        return return_lst
    
    def get_type(self):
        return self.matrix_type
    
    def get_most_causal_pair(self, rank = 0):
        return self.matrix_sorted_list[rank]
    
    def sort_matrix(self):
        self.matrix_sorted_list = [(c,i) for c, i, v in self.sort_Tuple([(k,v,self.get_Value((k,v))) for k,v in self.matrix_list])]
            
    def sort_Tuple(self,tup): 
        tup.sort(key = lambda x: x[2]) 
        return tup 

    def tolist(self):
        if len(self.matrix_list) == 0:
            for col in self.df.columns.values.tolist()[1:]:
                for idx in self.df.columns.values.tolist()[1:]:
                    self.matrix_list.append((col,idx))
        return self.matrix_list

    def get_interesting_result(self, effect_cond = ""):
        for pair in self.matrix_sorted_list:
            if pair[0] != pair[1] and effect_cond in pair[0] and not math.isnan(float(self.get_Value(pair))):
                self.interesting_results.append(pair)
        self.interesting_results.reverse()
    
    def sum_col(self, col):
        return sum(list(self.df[col]))
    
    def matrix_sum(self):
        return sum([self.sum_col(col) for col in self.df.columns.values.tolist()[1:]])
    
    def translate(self, event):
        return self.mapper[event]
    
    def translate_causal_pairs(self):
        for pair in self.interesting_results:
            self.translated_pairs.append((pair[0],self.translate(pair[1])))
    
    def calculate_exp(self,avg,value):
        return int((avg*(1+(value/100))))
    
    def adjust_score(self,avg , cause_effect, exp_range):
        if not isinstance(cause_effect, str):
            for value in cause_effect:
                if self.calculate_exp(avg,value) in range(exp_range[0], exp_range[1]):
                    self.score += 1
    
    def count_actual_causality(self, K, avg = 3259):
        used_pair = []
        for i in range(len(self.interesting_results[:K])):
            translated_effect = self.translated_pairs[i][0]
            traffic_range = self.event_to_value[translated_effect]
            cause_effect = self.translated_pairs[i][1][:-1]
            if not (translated_effect, cause_effect) in used_pair:
                used_pair.append((translated_effect, cause_effect))
                self.adjust_score(avg, cause_effect, traffic_range)


def get_csv_files_containing(path, score):
    files = []
    for file in os.listdir(path):
        if file.endswith(".csv") and score in file:
            files.append(file)
    return files

def load_matrixes(path, score):
    matrixs_lst = []
    files = get_csv_files_containing(path, 'cir_c')
    for file in files:
        matrixs_lst.append(result_matrix(path+'\\'+file,matrix_type = file))
    matrixs_lst.sort(key=lambda x: x.interesting_sum, reverse=True)
    return matrixs_lst

def calculate_matrixes_causality(matrixs_lst,k):
    for matrix in matrixs_lst:
        matrix.count_actual_causality(k)



if __name__ == '__main__':
    path = 'BiksCalculations\\results\\no_cluster'
    matrixes = load_matrixes(path,'cir_c')
    calculate_matrixes_causality(matrixes,20)
    matrixs_lst.sort(key=lambda x : x.score)

    print(matrixs_lst[-1].score)
    for things in matrixs_lst[-1].interesting_results[:15]:
        print(f"{things},  {matrixs_lst[-1].get_Value(things)}")
