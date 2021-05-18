from numpy.lib.shape_base import split
import pandas as pd
from datetime import datetime
import numpy as np
from numpy import  c_, random
import os
import random as rand
from string import ascii_lowercase
from copy import deepcopy
import pandas as pd
import csv
from pandas.core.frame import DataFrame

from pandas.core.indexes import base

class cluster_class():
    def __init__(self, size:tuple, cause:list, prob:list):
        self.size = size
        self.cause = cause
        self.prob = prob

# def label_gen(e_num:int) -> list: 
#     """Generate labels

#     Args:
#         e_num (int): [Number of Event labels]

#     Returns:
#         list: [list of labels]
#     """
#     label_lst = []
#     for i in range(e_num):
#         label_lst.append(ascii_lowercase[i])
#         # print(label_lst[i])
#     return label_lst    




# def cause_gen(p_num:int, label_lst:list) -> dict:
#     """Generate DAG

#     Args:
#         p_num (Int): [Number of Event-Pairs]
#         label_lst (list): [All unique labels]

#     Returns:
#         dict: [Dag, where the key is Parent and value is Child]
#     """
#     e_dict = {}
#     weights = []
#     # generate even distributed wieghts 
#     for i in range(len(label_lst)): 
#         weights.append(1/len(label_lst))
#     # generate DAG where choice for children adhere to weights 
#     for i in range(p_num):
#         # rng = random.randint(0,len(label_lst))
#         e_dict[label_lst[i]] = rand.choices(label_lst, weights)
#     return e_dict

# def prob_dist(e_num:int,label_lst:list,e_dict:dict,c_weight:float) -> dict:
#     """Distribute list of weights to each parent 

#     Args:
#         e_num (int): [Number of parents]
#         label_lst (list): [List of labels]
#         e_dict (dict): [DAG from cause_gen method]

#     Returns:
#         dict: [DAG with weighted distribution]
#     """
#     repli_dict = e_dict.copy()
#     # repli_dict.update(e_dict)
#     # Initialize a probability distribution
#     prob_list = []
#     for i in range(e_num):
#         prob_list.append(1/e_num)

#     # Merge label list with probability distribution
#     e_dist_list = [[label_lst[i],prob_list[i]] for i in range(0,len(prob_list))]

#     # Assign probability distribution to DAG
#     for e in e_dist_list:
#         repli_dict[e[0]] = deepcopy(e_dist_list)
    
#     # Change Weights according to DAG
#     for i in e_dict.keys():
#         if repli_dict[i] is not None:
#             for e in e_dict[i]:
#                 for ind,j in enumerate(repli_dict[i]):
#                     if e == j[0]:
#                         repli_dict[i][ind][1] = (c_weight/len(e_dict[i]))
#                     else:
#                         #(1-c_weight)/((len(repli_dict[i])-len(e_dict[i])))
#                         repli_dict[i][ind][1] = 0
#     return repli_dict

#Time Horizon
# def horizon(ts:int = 0,te:int = 1000,step:int = 60) -> list: return np.arange(ts,te,step)

# def yield_prob(e_dict, e_num:int, w_size:int) -> list:
#     pass
    # print('x',e_dict)
    # total_t = horizon()[-1]
    # prob_dict = {}
    # event_list = []
    # weights = [1,1,1,1,10]
    # labels =['a','b','c','d','e']
    # for i in range(total_t):
    #     event_list.append(np.random.choice(labels,weights))
    #     event_list.append(i)
    # return prob_dict

# def calc_probability(prob_list, change_prob):
#     for c_p in change_prob:
#         prob_dist 

def initiate_beginning_probs(num_events):
    prob_list = []
    for i in range(num_events):
        prob_list.append(1/num_events)
    return prob_list

def calc_next_event(prob_list, base_prob):
    c = list(prob_list.keys())
    return rand.choices(c,base_prob)

# def process_prev_events(prev_events, prob_list, base_prob):
#     even_prob = []
#     for i, e in enumerate(prev_events):
#             t = i+1
#             for ind, pb in enumerate(prob_list[e[0]]):
#                 if pb[1] != 0:
#                     temp_prob = deepcopy(base_prob)
#                     #prob = (base_prob[ind]*pb[1]) * (t/len(prev_events))
#                     temp_prob[ind] = base_prob[ind]+prob
#                     #even_lower = (prob/(len(temp_prob)-1))
#                     for i_c, c_percentage in enumerate(base_prob):
#                         if i_c != ind:
#                             temp_prob[i_c] = (((c_percentage-prob/(len(temp_prob)-1)))*(t/len(prev_events)))
#                     even_prob.append(temp_prob)
#     return even_prob


# def calc_next_prob(prob_list, n_event, base_prob, prev_events):
#     #cur_prob = process_prev_events(prev_events, prob_list, base_prob)
#     cur_prob = []
#     prob_dist = []
#     next_prob = []
#     count = 0

#     for probs in cur_prob:
#         for ind, prob in enumerate(probs):
#             if len(next_prob) < len(probs):
#                 next_prob.append(prob)
#             else:
#                 next_prob[ind] = next_prob[ind] + prob

#     for ind, prob in enumerate(next_prob):
#         next_prob[ind] = prob/len(cur_prob)
        
    # for c_b in cur_prob:
    #     t_c_b = []
    #     for ind, var in enumerate(c_b):
    #         if not prob_dist:
    #             t_c_b.append(c_b[ind])
    #         else:
    #             prob_dist[ind] = prob_dist[ind] + c_b[ind]
    #     prob_dist.append(t_c_b)
    #     count += 1
    # print('prob_dist', prob_dist)
    # for var in prob_dist:
    #     print(var[1])
    # return next_prob

# def cycle_events(prev_events, n_event, win_size):
#     if len(prev_events) < win_size:
#         prev_events.append(n_event)
#     else:
#         prev_events.pop(0)
#         prev_events.append(n_event)
#     return prev_events

# def calc_event_list(prob_list, row_num, win_size):
#     base_prob = initiate_beginning_probs(len(prob_list.keys()))
#     next_prob = deepcopy(base_prob)
#     event_arr = []
#     prev_events = []
    
    # for r in range(row_num):
    #     n_event = calc_next_event(prob_list, next_prob)
    #     event_arr.append(n_event[0])
    #     # prev_events = cycle_events(prev_events,n_event,win_size)
    #     # next_prob = calc_next_prob(prob_list, n_event, base_prob, prev_events)
    
    # return event_arr

def get_mean_from_prob(prob_arr):
    prob_val = [0 for x in range(len(prob_arr[0]))]
    for prob in prob_arr:
        for ind, val in enumerate(prob):
            prob_val[ind] += val
    for e, val in enumerate(prob_val):
        prob_val[e] = (val/len(prob_arr))
    return prob_val

def get_prob_from_cl_dict(cluster_dict, prev_clust):
    prob_arr = []
    for p_cl in prev_clust:
        prob_val = [0 for x in range(len(cluster_dict))]
        even_num = 0
        for ind, cause in enumerate(cluster_dict[p_cl[0]].cause):
            if cause == '':
                break
            prob_index = list(cluster_dict.keys()).index(cause)
            even_num += cluster_dict[p_cl[0]].prob[ind]
            prob_val[prob_index] = (cluster_dict[p_cl[0]].prob[ind])
            if even_num >= 1:
                print('Warning: Percentage above 100%, error will occur in the generation.')
        find_consensus = (1-even_num)/(len(cluster_dict)-len(cluster_dict[p_cl[0]].cause))
        for ind, t_prob in enumerate(prob_val):
            if t_prob == 0:
                prob_val[ind] = find_consensus
        prob_arr.append(prob_val)
    return prob_arr


def calc_prob_arr(cluster_dict,prev_clust, base_prob):
    cl_prob_arr = get_prob_from_cl_dict(cluster_dict,prev_clust)
    m_p_arr = get_mean_from_prob(cl_prob_arr)
    for ind, b_p in enumerate(base_prob):
        base_prob[ind] = (b_p + m_p_arr[ind])/2
    return base_prob

def cycle_clust(prev_clust, n_clust, win_size):
    if len(prev_clust) < win_size:
        prev_clust.append(n_clust)
    else:
        prev_clust.pop(0)
        prev_clust.append(n_clust)
    return prev_clust

def calculate_next_cluster(cluster_dict,prob_arr,prev_event):
    vals = []
    if prev_event: 
        vals = [key for key, value in cluster_dict.items() if prev_event[0].split("_")[0] in key.lower()]
        for v in vals:
            ind = list(cluster_dict.keys()).index(v)
            prob_arr[ind] = 0

    return rand.choices(list(cluster_dict.keys()),prob_arr)
    

def calc_ini_prob(size:int):
    return np.full(size, 1/size)

def process_cluster_arrays(cluster_dict:dict, num_rows:int, win_size:int):
    base_prob = calc_ini_prob(len(cluster_dict))
    prob_arr = deepcopy(base_prob)
    prev_event = ''
    prev_clust = []
    clust_arr = []
    for r in range(num_rows):
        n_clust = calculate_next_cluster(cluster_dict, prob_arr,prev_event)
        prev_event = n_clust
        clust_arr.append(n_clust)
        prev_clust = cycle_clust(prev_clust,n_clust,win_size)
        prob_arr = calc_prob_arr(cluster_dict,prev_clust,base_prob)
    return clust_arr

def transform_cl_to_events(c_list, cluster_dict):
    e_list,e_cl_list = [], []
    for c in c_list:
        e_name = c[0].split("_")[0]
        num_events = cluster_dict[c[0]].size[rand.randint(0,1)]
        for r in range(num_events):
            e_list.append(e_name)
            e_cl_list.append(c[0])
    return e_list, e_cl_list


def create_time_serie(period):
    dt = pd.date_range(datetime.today().strftime('%Y-%m-%d'), periods=period, freq="H")
    return pd.date_range(datetime.today().strftime('%Y-%m-%d'), periods=period, freq="H")

def combine_time_event(e_list, c_list, tdf):
    e_df = pd.DataFrame({'time_set': tdf, 'events': e_list}, columns=['time_set', 'events'])
    c_df = pd.DataFrame({'time_set': tdf, 'events': e_list, 'events_cluster': c_list}, columns=['time_set', 'events', 'events_cluster'])
    return e_df, c_df

def generate_rows(cluster_dict, period, win_size):
    c_list = process_cluster_arrays(cluster_dict,period,win_size)
    e_list, e_cl_list = transform_cl_to_events(c_list,cluster_dict)
    tdf = create_time_serie(period)
    return combine_time_event(e_list[:period], e_cl_list[:period], tdf)

def create_csv(df:DataFrame,path:str): 
    df.to_csv(path)

def initiate_generation(output_path:str, cluster_dict:dict, period_days:int, window_size:int):
    period = int(period_days * 24)
    e_df, c_df = generate_rows(cluster_dict,period,window_size)
    create_csv(e_df,output_path)
    create_csv(c_df,'temp.csv')

def run():
    pass

if __name__ == '__main__':
    input_dict = {
        'a_0': cluster_class((6,10), ['b_0'], [0.8]),
        'a_1': cluster_class((30,36), ['b_1'], [0.8]),
        'a_2': cluster_class((70,75), ['b_1'], [0.8]),
        'b_0': cluster_class((3,4), ['c_0'], [0.8]),
        'b_1': cluster_class((10,12), ['c_1'], [0.8]),
        'b_2': cluster_class((21,23), ['c_2'], [0.8]),
        'c_0': cluster_class((1,4), ['e_0'], [0.4]),
        'c_1': cluster_class((15,18), ['d_0'], [0.3,0.4]),
        'c_2': cluster_class((31,34), ['d_0'], [0.2,0.5]),
        'd_0': cluster_class((5,12), ['e_0'], [0.3]),
        'e_0': cluster_class((2,5), [''], [0])
    }

    initiate_generation('test.csv',input_dict,365,1)

    # events = {'a': [['a',0],['b',0.5],['c',0]],
    #           'b': [['a',0],['b',0],['c',0.5]],
    #           'c': [['a',0.5],['b',0],['c',0]]}
    # years = 1
    # win_size = 5

    # initiate_generation('test.csv')
