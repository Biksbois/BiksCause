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
        self.comprehension_list = []
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
            print(self.matrix_sorted_list)
            #print(len(self.interesting_results))
            self.interesting_sum = sum(self.get_list_Value(self.interesting_results))
            self.translate_causal_pairs()
        if 'air' in self.matrix_type:
            seasons = ['winter','summer','spring','fall']
            for season in seasons:
                if season in self.matrix_type:
                    self.season = season
                    break;

    def extract_file_config(self, file):
        alpha_regex,lambda_regex,header_regex,window_regex = ('_a(\d+|\d+.\d)_','_l(\d+|\d+.\d)_','_h\d+_','_w\d+_')
        self.window = re.search(window_regex,file).group().replace('_','').replace('w','')
        self.header = re.search(header_regex,file).group().replace('_','').replace('h','')
        if('cir' not in file):
            self.lamb = int(float(re.search(lambda_regex,file).group().replace('_','').replace('l',''))/10)
            self.alpha = int(float(re.search(alpha_regex,file).group().replace('_','').replace('a',''))/100)

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
                print(value)
                if self.calculate_exp(avg,value) in range(exp_range[0], exp_range[1]):
                    self.score += 1

    def count_actual_causality(self, K, avg = 3259):
        #used_pair = []
        for i in range(len(self.interesting_results[:K])):
            translated_effect = self.translated_pairs[i][0]
            traffic_range = self.mapper_obj.event_to_value[translated_effect]
            cause_effect = self.translated_pairs[i][1][:-1]
            # if not (translated_effect, cause_effect) in used_pair:
            #     used_pair.append((translated_effect, cause_effect))
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
        self.matrix_sorted_list.reverse()
        found = self.matrix_sorted_list[:k]
        truths = self.Convert_ground_truth(groundtruth)
        if self.cluster_stat == "no_cluster":
            found = list(set(self.translate_to_non_cluster(found)))
            truths = list(set(self.translate_to_non_cluster(truths)))
        for truth in truths:
            if truth in found:
                counter += 1
        self.score = counter
        
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
        # used_pair = []
        strings = []
        #print(len(self.))
        for i in range(len(self.interesting_results[:K])):
            translated_effect = self.translated_pairs[i][0]
            traffic_range = self.mapper_obj.event_to_value[translated_effect]
            cause_effect = self.translated_pairs[i][1][:-1]
            strings.append(self.get_calc_string(avg, cause_effect, traffic_range,self.interesting_results[i],i))
        return strings
    
    def get_calc_string(self,avg,cause_effect,traffic_range,pair,count):
        results = []
        if not isinstance(cause_effect, str):
            count +=1
            for value in cause_effect:
                res = avg*(1+(value/100))
                if (int(res) in range(traffic_range[0], traffic_range[1])):
                    results.append(f"\\rowcolor{{lightgray}} {count} & {pair[0].replace('_', '')} & {pair[1].replace('_', '')} & $({avg}*(1+({value}/100))) = {int(res)} \\in {traffic_range}$\\\\")
                else:
                    results.append(f"{count} & {pair[0].replace('_', '')} & {pair[1].replace('_', '')} & $({avg}*(1+({value}/100))) = {int(res)} \\in {traffic_range}$\\\\")
        else:
            count +=1
            results.append(f"{count} & {pair[0].replace('_', '')} & {pair[1].replace('_', '')} & $({avg}*(1+(-1))) = {0} \\in {traffic_range}$\\\\")
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
    print(path)
    matrixes = load_matrixes(path,score,k=k,maps = maps,window=window,heads=heads)
    print(len(matrixes))
    calculate_matrixes_causality(matrixes,k)
    matrixes.sort(key=lambda x : x.score)
    calcs = matrixes[-1].get_calc_ac(k)
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
        results.append((types, avg, scores))
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
        merged_matrixes.append(merge_season_results(hyper_dict[key],k,key))
    for matrix in merged_matrixes:
        result_matrixes.append(sorted(matrix, key=lambda x: x[2]))
    for m in result_matrixes:
        m.reverse()
        #print(m[:k])
        #print(count_air_cause(m[:k]))
    print(get_seasons_average())
    exit()
    return count_air_cause(result_matrixes)

def refactored_air_experiment(path,k,score,groundtruth,window=None,heads=None):
    matrixes = load_matrixes(path,score,k=k,window=window,heads=heads)
    grouped_matrixes = group_matrixes(matrixes)
    grouped_result_matrixes = calculate_group_causality(grouped_matrixes,k)
    result_list = merge_result_matrixes(grouped_result_matrixes)
    most_causal_list = select_most_causal(result_list,k)
    print_top_k(most_causal_list,k)

def print_top_k(lst,k):
    with open(f'BiksCalculations\\air_results\{lst[0]}.txt', 'w') as f:
        write = csv.writer(f)
        # usedpairs = []
        for entry in lst[1][:k]:
            # pair = (entry[0][0][0],split_on_underscore(entry[0][0][1]),entry[2])
            # if pair not in usedpairs:
            print(entry)
            write.writerow(entry)
                # usedpairs.append(pair)

def select_most_causal(reslut_lst,k):
    counts = []
    #usedpairs = []
    for lst in reslut_lst:
        count = 0
        for entry in lst[1][:k]:
            # pair = (entry[0][0][0],split_on_underscore(entry[0][0][1]),entry[2])
            # if pair not in usedpairs:
            #     usedpairs.append(pair)
            if entry[0][1]:
                count += 1
        #usedpairs = []
        print(count)
        counts.append(count)
    return reslut_lst[explicit(counts)]

def explicit(l):
    max_val = max(l)
    max_idx = l.index(max_val)
    return max_idx

def count_causal_in_k(lst, k):
    print(lst[1][0])
    for element in lst[0][1][:k]:
        if element[0][1]:
            print(element)
        

def merge_result_matrixes(groups):
    Matrix_results = []
    for key in groups.keys():
        Matrix_results.append((key,merge_lists(groups[key])))
    return Matrix_results
            
def merge_lists(group):
    res = []
    for member in group:
        for element in member.comprehension_list:
            res.append((element,member.get_Value(element[0]),member.season))
    res = sorted(res, key=lambda x: x[1])
    res.reverse()
    return res

def calculate_group_causality(groups,k):
    for key in groups.keys():
        groups[key] = calcualte_matrix_causalty(groups[key],k)
    return groups

def calcualte_matrix_causalty(matrix_group, k):
    return_matrixes = []
    for matrix in matrix_group:
        season = matrix.season
        #matrix.interesting_results.reverse()
        # for m in matrix.interesting_results:
        #     print(matrix.get_Value(m))
        for element in matrix.interesting_results[:k]:
            if is_air_causal(season, element):
                matrix.comprehension_list.append((element,True))#add tuple containing truth and season, and pair
            else:
                matrix.comprehension_list.append((element,False))
        return_matrixes.append(matrix)
    return return_matrixes
            
def is_air_causal(season, pair):
    avg_PM10 = get_season_avg(season)
    coefficient = get_season_coefficient(season,pair[1])
    PM = get_PM_range(pair[0])
    if int(avg_PM10*(1+coefficient)) in PM:
        return True
    else:
        return False
    
def get_PM_range(PM):
    PM_mapping = {
        'PM10_0': range(1,104),
        'PM10_1': range(105,260),
        'PM10_2': range(261,500)
    }
    return PM_mapping[PM]
    
def group_matrixes(matrixes):
    hyper_dict = {}
    for matrix in matrixes:
        if matrix.generate_matrix_key() not in hyper_dict.keys():
            hyper_dict[matrix.generate_matrix_key()] = []
        matrix.get_interesting_result(effect_cond="PM10")
        hyper_dict[matrix.generate_matrix_key()].append(matrix) 
    return hyper_dict

def get_season_coefficient(season, weather):
    season_weather_dict = {
        'summer': {
            'TEMP':0.40,
            'PRES':-0.05,
            'DEWP':0.04,
            'WSPM':-0.11,
            },
        'winter':  {
            'TEMP':0.30,
            'PRES':-0.45,
            'DEWP':0.50,
            'WSPM':-0.33,
            },
        'fall':  {
            'TEMP':0.38,
            'PRES':-0.40,
            'DEWP':0.53,
            'WSPM':-0.45,
            },
        'spring':  {
            'TEMP':0.45,
            'PRES':-0.45,
            'DEWP':0.13,
            'WSPM':-0.18,
            }
    }
    if split_on_underscore(weather) in season_weather_dict[season]: 
        return season_weather_dict[season][split_on_underscore(weather)]
    else:
        return -1
    
    

def get_seasons_average():
    results = {}
    seasons = ['summer','winter','fall','spring']
    for season in seasons:
        results[season] = get_season_avg(season)
    return results
    
def get_season_avg(season):
    path = f"input_csv\PRSA_Data_Dongsi_{season}.csv"
    panda = pd.read_csv(path)
    average = panda['PM10'].mean()
    return average

def count_air_cause(matrixes):
    res=0
    for element in matrixes:
        if element[3] == 1:
            res += 1
    return res
    
    

def merge_season_results(matrixes,k,key):
    res = []
    for matrix in matrixes:
        used_pair = []
        for x in matrix.interesting_results[:k]:
            if not x in used_pair:
                used_pair.append(x)
                causal = is_causal(matrix.season,x,matrix.cluster_stat)
                res.append((matrix.season,x,matrix.get_Value(x),causal,key))
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
    
def split_on_underscore(cause):
    cause_lst = cause.split('_')
    return cause_lst[0]


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
    }

def save_matrix_results(matrix_result): 
    with open(f'BiksCalculations\synthetic_avg_results\{matrix_result[0]}.txt', 'w') as f:
        write = csv.writer(f)
        
        write.writerow(matrix_result[2])

def generate_air_tables():
    basepath = 'BiksCalculations\\air_results'
    paths = find_air_results(basepath)
    files = load_files_air(paths,basepath)
    for entry in files:
        print('______________________________')
        generate_air_table(entry)

def generate_air_table(string):
    lst = string[0].split('  ')
    print(string[1])
    for i,s in enumerate(lst):
        if not len(s)<1:
            print(calc_air_table_str(extract_aspects_air(s),i+1))

def calc_air_table_str(info,count):
    avg = get_season_avg(info[1])
    value = get_season_coefficient(info[1], info[0][1])
    res = avg*(1+value)
    if info[2] == 'True':
        return(f"\\rowcolor{{lightgray}} {count} & {info[0][0]} & {info[0][1]} & $({int(avg)}*(1+({value}))) = {int(res)} \\in {get_PM_range(info[0][0])}$\\\\")
    else:
        return(f"{count} & {info[0][0]} & {info[0][1]} & $({int(avg)}*(1+({value}))) = {int(res)} \\in {get_PM_range(info[0][0])}$\\\\")
        
    
def extract_aspects_air(line):
    caused_regex = "'.+',"
    causal_regex = ", '.+'"
    season_regex = "\w+$"
    is_true_regex = "(True|False)"
    caused = re.findall(caused_regex, line)[0]
    causal = re.findall(causal_regex, line)[0]
    season = re.findall(season_regex, line)[0]
    is_true = re.findall(is_true_regex, line)[0]
    caused = caused[1:-2]
    causal = causal[3:-1]
    pair = (caused,causal)
    return (pair,season,is_true)

def generate_table_line(line):
    res = ''
    if 'True' in line:
        pass
    else:
        pass

def load_files_air(lst,basepath):
    air_files = []
    
    for path in lst:
        file = open(basepath+'\\'+path)
        line = file.read().replace("\n", " ")
        file.close()
        air_files.append((line,path))
    return air_files

def find_air_results(path):
    files = []
    for file in os.listdir(path):
        if file.endswith(".txt"):
            files.append(file)
    return files

if __name__ == '__main__':

    path = 'BiksCalculations\\results\\synthetic\\cluster'
    maps = 'traffic_cluster'
    # print(get_at_k_hits(path,20,'cir', maps,window=[18,12], heads=[50000]))
    print(run_average_expriment(path,20,'nst', maps,window=[18,12], heads=[50000]))

