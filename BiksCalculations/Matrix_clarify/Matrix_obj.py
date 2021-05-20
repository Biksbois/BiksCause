import pandas as pd
import os
import re
import math
import csv
from BiksCalculations.Matrix_clarify.mapper import *
from BiksPrepare.synthetic_generator import cluster_class


class result_matrix():
    def __init__(self, path, mapper_dict, k = 0, matrix_type = 'unspecified', mapper_cat = "", score_type = ""):
        self.df = pd.read_csv (path)
        self.create_label_mapping(self.df)
        self.cluster_stat = self.cluster_status(path)
        self.matrix_type = matrix_type
        self.matrix_list = []
        self.matrix_sorted_list = []
        self.interesting_results = []
        self.interesting_sum = []
        self.translated_pairs = []
        self.score_type = score_type
        self.extract_file_config(path)
        self.k = k
        self.key =""
        self.score = 0
        if 'traffic' in self.matrix_type:
            self.mapper_obj = mappers(mapping_cat = "traffic")
            self.custom_mapper = self.mapper_obj.mapper_dict[mapper_dict]
        self.initialize_lists()
        
    def cluster_status(self, path):
        if "no_cluster" in path:
            return "no_cluster"
        return "cluster"
    def initialize_lists(self):
        self.tolist()
        self.sort_matrix()
        if 'traffic' in self.matrix_type:
            self.get_interesting_result("traffic")
            self.interesting_sum = sum(self.get_list_Value(self.interesting_results))
            self.translate_causal_pairs()
        if 'air' in self.matrix_type:
            seasons = ['winter','summer','spring','fall']
            for season in seasons:
                if season in self.matrix_type:
                    self.season = season
                    break;

    def extract_file_config(self, file):
        alpha_regex,lambda_regex,header_regex,window_regex = ('_a\d+_','_l\d+_','_h\d+_','_w\d+_')
        self.window = re.search(window_regex,file).group().replace('_','').replace('w','')
        self.header = re.search(header_regex,file).group().replace('_','').replace('h','')
        if('cir' not in file):
            self.lamb = int(re.search(lambda_regex,file).group().replace('_','').replace('l',''))/10
            self.alpha = int(re.search(alpha_regex,file).group().replace('_','').replace('a',''))/100

    def create_label_mapping(self,df):
        self.lookup_dict = {}
        for i, head in enumerate(self.df.columns.values.tolist()):
            self.lookup_dict[head] = i

    def get_Value(self,pair):
        col,idx = pair
        if idx in self.lookup_dict.keys():
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
                    if self.get_Value((col,idx)) != 0:
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
        return self.custom_mapper[event]

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
            traffic_range = self.mapper_obj.event_to_value[translated_effect]
            cause_effect = self.translated_pairs[i][1][:-1]
            if not (translated_effect, cause_effect) in used_pair:
                used_pair.append((translated_effect, cause_effect))
                self.adjust_score(avg, cause_effect, traffic_range)

    def remove_cluster_def(self, string):
        regex = re.compile('[^a-zA-Z]')
        return regex.sub('', string)
    
    def translate_to_non_cluster(self, pairs):
        result = []
        for pair in pairs:
            result.append((self.remove_cluster_def(pair[0]),self.remove_cluster_def(pair[1])))
        return result
    
    def Convert_ground_truth(self, ground_truth):
        causal_pairs = []
        for key in ground_truth.keys():
            for value in ground_truth[key].cause:
                causal_pairs.append((key,value))
        return causal_pairs
    
    def Count_causal_pair_from_groundtruth(self, groundtruth, k=10):
        counter = 0
        found = self.matrix_sorted_list[:k]
        truths = self.Convert_ground_truth(groundtruth)
        #print(f"There are {len(truths)} ground truths")
        print(f"These are the ground truetsh {truths}")
        print(f"These are the the found causal pairs {found}")
        if self.cluster_stat == "no_cluster":
            found = list(set(self.translate_to_non_cluster(found)))
            truths = list(set(self.translate_to_non_cluster(truths)))
        for truth in truths:
            if truth in found:
                counter += 1
                print(f"Is found {truth}")
            else:
                print(f"{truth} is not found")
        self.score = counter

        # print(self.matrix_sorted_list[:1])
        # print("___________________")
        # print(f"{self.matrix_type}")
        # print(f"result: {counter}")
        # print(f"groundtruths: {truths}")
        # print(f"found: {found}")
    # def generate_hyper_key(self):
    #     hyper_key = self.window+self.header
    #     if 'nst' in self.score_type:
    #         hyper_key += 
        
    def generate_matrix_key(self):
        if self.key == "":
            std_key = self.score_type +'_w'+ self.window +'_h'+ self.header
            if 'nst' in self.score_type:
                std_key += '_l'+str(self.lamb) +'_a'+ str(self.alpha)
            self.key = std_key
        else:
            std_key = self.key
        return std_key+'_k'+str(self.k)+'_'+self.cluster_stat
            
    def get_calc_ac(self,K,avg = 3259):
        used_pair = []
        strings = []
        for i in range(len(self.interesting_results[:K])):
            translated_effect = self.translated_pairs[i][0]
            traffic_range = self.mapper_obj.event_to_value[translated_effect]
            cause_effect = self.translated_pairs[i][1][:-1]
            if not (translated_effect, cause_effect) in used_pair:
                used_pair.append((translated_effect, cause_effect))
                strings.append(self.get_calc_string(avg, cause_effect, traffic_range,self.interesting_results[i]))
        return strings
    
    def get_calc_string(self,avg,cause_effect,traffic_range,pair):
        results = []
        if not isinstance(cause_effect, str):
            for value in cause_effect:
                res = avg*(1+(value/100))
                if (int(res) in range(traffic_range[0], traffic_range[1])):
                    results.append(f"\\rowcolor{{lightgray}} {pair[0].replace('_', '')} & {pair[1].replace('_', '')} & $({avg}*(1+({value}/100)))) = {int(res)} \\in {traffic_range}$\\\\")
                else:
                    results.append(f"{pair[0].replace('_', '')} & {pair[1].replace('_', '')} & $({avg}*(1+({value}/100)))) = {int(res)} \\in {traffic_range}$\\\\")
                    
        return results
        
def get_csv_files_containing(path, score):
    files = []
    for file in os.listdir(path):
        if file.endswith(".csv") and score in file:
            files.append(file)
    return files

def load_matrixes(path, score, k=0, maps = "", window=None, heads=None):
    if not window == None:
        window = map(str,window)
        window = ['w'+ w for w in window]
    if not heads == None:
        heads = map(str,heads)
        heads = ['h'+ h for h in heads]
    matrixs_lst = []
    files = get_csv_files_containing(path, score)
    for file in files:
        if (not window == None and not any(x in file for x in window)) or (not heads == None and not any(x in file for x in heads)):
            continue
        matrixs_lst.append(result_matrix(path+'\\'+file,maps,k=k,matrix_type = file, score_type = score))
    matrixs_lst.sort(key=lambda x: x.interesting_sum, reverse=True)
    return matrixs_lst

def calculate_matrixes_causality(matrixs_lst,k):
    for matrix in matrixs_lst:
        matrix.count_actual_causality(k)

def get_at_k_hits(path, k, score,maps, window=None, heads=None):
    matrixes = load_matrixes(path,score,maps = maps,window=window,heads=heads)
    calculate_matrixes_causality(matrixes,k)
    matrixes.sort(key=lambda x : x.score)
    calcs = matrixes[-1].get_calc_ac(10)
    save_in_text(calcs,matrixes[-1].generate_matrix_key())
    return matrixes[-1].score    

def save_in_text(lst, name):
    textfile = open(f"BiksCalculations\Calculations_for_roni\{name}.txt", "w")
    for element in lst:
        if(len(element) != 0):
            textfile.write(element[0] + "\n")
    textfile.close()
    
def group_same_attr_matrixes(matrixes):
    matrix_types = {}
    for matrix in matrixes:
        if matrix.generate_matrix_key() not in matrix_types:
            matrix_types[matrix.generate_matrix_key()] = []
        matrix_types[matrix.generate_matrix_key()].append(matrix)
    return matrix_types

def comp_matrix_score(matrix_types, k, groundtruth):
    results = []
    for types in matrix_types.keys():
        avg,scores = avg_scores_matrix_list(matrix_types[types],groundtruth, k=k)
        results.append((types,avg, scores))
    return results

def avg_scores_matrix_list(matrixes, groundtruth, k = 10):
    avg_score = 0
    scores = []
    for matrix in matrixes:
        matrix.Count_causal_pair_from_groundtruth(groundtruth, k=k)
        scores.append(matrix.score)
        avg_score += matrix.score
    return (avg_score/len(matrixes),scores)

def average_score_all_matrixes(matrixes,k, groundtruth):
    gm = group_same_attr_matrixes(matrixes)
    return comp_matrix_score(gm,k, groundtruth)

def run_average_expriment(path, k, score,groundtruth, window=None, heads=None):
    matrixes = load_matrixes(path,score,k=k,window=window,heads=heads)
    avg_scores = average_score_all_matrixes(matrixes,k, groundtruth)
    avg_scores = sorted(avg_scores,key=lambda x: x[1])
    save_matrix_results(avg_scores[-1])
    return avg_scores[-1]

def air_experiment_results(path,k,score,groundtruth,window=None, heads=None):
    hyper_dict = {}
    merged_matrixes = []
    result_matrixes = []
    matrixes = load_matrixes(path,score,k=k,window=window,heads=heads)
    for matrix in matrixes:
        if matrix.generate_matrix_key() not in hyper_dict.keys():
            hyper_dict[matrix.generate_matrix_key()] = []
        matrix.get_interesting_result(effect_cond="PM10")
        hyper_dict[matrix.generate_matrix_key()].append(matrix) 
    for key in hyper_dict.keys():
        merged_matrixes.append(merge_season_results(hyper_dict[key],k))
    for matrix in merged_matrixes:
        result_matrixes.append(sorted(matrix, key=lambda x: x[2]))
    for m in result_matrixes:
        m.reverse()
        # print(m[:k])
        print(count_air_cause(m[:k]))
        
        #print(m[:k])
    return count_air_cause(result_matrixes)

def count_air_cause(matrixes):
    res=0
    for element in matrixes:
        if element[3] == 1:
            res += 1
    return res
    
    

def merge_season_results(matrixes,k):
    res = []
    for matrix in matrixes:
        used_pair = []
        for x in matrix.interesting_results[:k]:
            if not x in used_pair:
                used_pair.append(x)
                causal = is_causal(matrix.season,x,matrix.cluster_stat)
                res.append((matrix.season,x,matrix.get_Value(x),causal,matrix.matrix_type))
    return res

def is_causal(season, pair, cluster_stat):
    PM10_level = pair[0]
    cause = pair[1]
    if cluster_stat == 'cluster':
        if 'PM10' not in cause:
            cause=remove_cluster_notation(cause)
    if  cause in causal_air_dic()[PM10_level].keys():
        return 1
    else:
        return 0
    
def remove_cluster_notation(cause):
    cause_lst = cause.split('_')
    cause = ''
    for string in cause_lst[:-1]:
        cause += string +'_'
    return cause[:-1]
    

def causal_air_dic():
    return {
        'PM10_0':{
            'PRES_1':True,
            'WSPM_1':True
            },
        'PM10_1':{
            'TEMP_1': True,
            'DEWP_1':True
        }
        
        # 'PM10_0':{
        #     'PRES_0':False,
        #     'PRES_1':True,
        #     'TEMP_0':False,
        #     'TEMP_1':False,
        #     'DEWP_0':True,
        #     'DEWP_1':False,
        #     'WSPM_0':False,
        #     'WSPM_1':True,
        #     'PM10_0':False,
        #     'PM10_1':False,
        #     'RAIN_0':False,
        #     'RAIN_1':False,
        #     'PM2.5_0':False,
        #     'PM2.5_1':False
        # }
        
    }
def save_matrix_results(matrix_result):    
    with open(f'BiksCalculations\synthetic_avg_results\{matrix_result[0]}', 'w') as f:
        write = csv.writer(f)
        
        write.writerow(matrix_result[2])


if __name__ == '__main__':

    path = 'BiksCalculations\\results\\synthetic\\cluster'
    maps = 'traffic_cluster'
    # print(get_at_k_hits(path,20,'cir', maps,window=[18,12], heads=[50000]))
    print(run_average_expriment(path,20,'nst', maps,window=[18,12], heads=[50000]))

