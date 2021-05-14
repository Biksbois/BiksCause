import pandas as pd
import os
import re
import math
from BiksCalculations.Matrix_clarify.mapper import *

class result_matrix():

    def __init__(self, path,mapper_dict, matrix_type = 'unspecified', mapper_cat = "", score_type = ""):
        self.df = pd.read_csv (path)
        self.create_label_mapping(self.df)
        self.matrix_type = matrix_type
        self.matrix_list = []
        self.matrix_sorted_list = []
        self.interesting_results = []
        self.interesting_sum = []
        self.translated_pairs = []
        self.score_type = score_type
        self.extract_file_config(path)
        self.key =""
        self.score = 0
        if mapper_cat == "traffic":
            self.mapper_obj = mappers(mapping_cat = mapper_cat)
            self.custom_mapper = self.mapper_obj.mapper_dict[mapper_dict]
        self.initialize_lists()
    def initialize_lists(self):
        self.tolist()
        self.sort_matrix()
        if 'traffic' in self.matrix_type:
            self.get_interesting_result("traffic")
            self.interesting_sum = sum(self.get_list_Value(self.interesting_results))
            self.translate_causal_pairs()

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
    
    def Count_causal_pair_from_groundtruth(self, groundtruth, k=10):
        counter = 0
        truths = self.exstract_comprehinsible_truth(groundtruth)
        found = self.translate_to_non_cluster(self.matrix_sorted_list[:k])
        for truth in truths:
            if truth in found:
                counter += 1
        # print(self.matrix_sorted_list[:1])
        print("___________________")
        print(f"result: {counter}")
        print(f"groundtruths: {truths}")
        print(f"found: {found}")
        
    
    def exstract_comprehinsible_truth(self, groundtruth):
        truths = []
        for truth in groundtruth.keys():
            for value in groundtruth[truth]:
                if value[1] > 0 and truth != value[0]:
                    truths.append((truth,value[0]))
        return truths
            
        
    def generate_matrix_key(self):
        if self.key == "":
            std_key = self.score_type + self.window + self.header
            if 'nst' in self.score_type:
                std_key += str(self.lamb) + str(self.alpha)
            self.key = std_key
        else:
            std_key = self.key
        return std_key

def get_csv_files_containing(path, score):
    files = []
    for file in os.listdir(path):
        if file.endswith(".csv") and score in file:
            files.append(file)
    return files

def load_matrixes(path, score, maps = "", window=None, heads=None):
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
        matrixs_lst.append(result_matrix(path+'\\'+file,maps,matrix_type = file, score_type = score))
    matrixs_lst.sort(key=lambda x: x.interesting_sum, reverse=True)
    return matrixs_lst

def calculate_matrixes_causality(matrixs_lst,k):
    for matrix in matrixs_lst:
        matrix.count_actual_causality(k)

def get_at_k_hits(path, k, score,maps, window=None, heads=None):
    matrixes = load_matrixes(path,score,maps,window=window,heads=heads)
    calculate_matrixes_causality(matrixes,k)
    matrixes.sort(key=lambda x : x.score)
    return matrixes[-1].score

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
        avg = avg_scores_matrix_list(matrix_types[types],groundtruth, k=k)
        results.append((types,avg))
    return results

def avg_scores_matrix_list(matrixes, groundtruth,k = 10):
    avg_score = 0
    for matrix in matrixes:
        matrix.Count_causal_pair_from_groundtruth(groundtruth)
        avg_score += matrix.score
    return avg_score/len(matrixes)

def average_score_all_matrixes(matrixes,k, groundtruth):
    gm = group_same_attr_matrixes(matrixes)
    return comp_matrix_score(gm,k, groundtruth)

def run_average_expriment(path, k, score,groundtruth, window=None, heads=None):
    matrixes = load_matrixes(path,score,window=window,heads=heads)
    return average_score_all_matrixes(matrixes[:1],k, groundtruth)


if __name__ == '__main__':

    path = 'BiksCalculations\\results\\synthetic\\cluster'
    maps = 'traffic_cluster'
    # print(get_at_k_hits(path,20,'cir', maps,window=[18,12], heads=[50000]))
    print(run_average_expriment(path,20,'nst', maps,window=[18,12], heads=[50000]))

