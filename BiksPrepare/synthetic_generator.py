import pandas as pd
from datetime import datetime
import numpy as np
from numpy import  random
import os
import random as rand
from string import ascii_lowercase
from copy import deepcopy
import pandas as pd
import csv
from pandas.core.frame import DataFrame

from pandas.core.indexes import base


def label_gen(e_num:int) -> list: 
    """Generate labels

    Args:
        e_num (int): [Number of Event labels]

    Returns:
        list: [list of labels]
    """
    label_lst = []
    for i in range(e_num):
        label_lst.append(ascii_lowercase[i])
        # print(label_lst[i])
    return label_lst    




def cause_gen(p_num:int, label_lst:list) -> dict:
    """Generate DAG

    Args:
        p_num (Int): [Number of Event-Pairs]
        label_lst (list): [All unique labels]

    Returns:
        dict: [Dag, where the key is Parent and value is Child]
    """
    e_dict = {}
    weights = []
    # generate even distributed wieghts 
    for i in range(len(label_lst)): 
        weights.append(1/len(label_lst))
    # generate DAG where choice for children adhere to weights 
    for i in range(p_num):
        # rng = random.randint(0,len(label_lst))
        e_dict[label_lst[i]] = rand.choices(label_lst, weights)
    return e_dict

def prob_dist(e_num:int,label_lst:list,e_dict:dict,c_weight:float) -> dict:
    """Distribute list of weights to each parent 

    Args:
        e_num (int): [Number of parents]
        label_lst (list): [List of labels]
        e_dict (dict): [DAG from cause_gen method]

    Returns:
        dict: [DAG with weighted distribution]
    """
    repli_dict = e_dict.copy()
    # repli_dict.update(e_dict)
    # Initialize a probability distribution
    prob_list = []
    for i in range(e_num):
        prob_list.append(1/e_num)

    # Merge label list with probability distribution
    e_dist_list = [[label_lst[i],prob_list[i]] for i in range(0,len(prob_list))]

    # Assign probability distribution to DAG
    for e in e_dist_list:
        repli_dict[e[0]] = deepcopy(e_dist_list)
    
    # Change Weights according to DAG
    for i in e_dict.keys():
        if repli_dict[i] is not None:
            for e in e_dict[i]:
                for ind,j in enumerate(repli_dict[i]):
                    if e == j[0]:
                        repli_dict[i][ind][1] = (c_weight/len(e_dict[i]))
                    else:
                        #(1-c_weight)/((len(repli_dict[i])-len(e_dict[i])))
                        repli_dict[i][ind][1] = 0
    return repli_dict

#Time Horizon
def horizon(ts:int = 0,te:int = 1000,step:int = 60) -> list: return np.arange(ts,te,step)

def yield_prob(e_dict, e_num:int, w_size:int) -> list:
    pass
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

def process_prev_events(prev_events, prob_list, base_prob):
    even_prob = []
    for i, e in enumerate(prev_events):
            t = i+1
            for ind, pb in enumerate(prob_list[e[0]]):
                if pb[1] != 0:
                    temp_prob = deepcopy(base_prob)
                    prob = (base_prob[ind]*pb[1]) * (t/len(prev_events))
                    temp_prob[ind] = base_prob[ind]+prob
                    even_lower = (prob/(len(temp_prob)-1))
                    for i_c, c_percentage in enumerate(base_prob):
                        if i_c != ind:
                            temp_prob[i_c] = (((c_percentage-prob/(len(temp_prob)-1)))*(t/len(prev_events)))
                    even_prob.append(temp_prob)
    return even_prob


def calc_next_prob(prob_list, n_event, base_prob, prev_events):
    cur_prob = process_prev_events(prev_events, prob_list, base_prob)
    prob_dist = []
    next_prob = []
    count = 0

    for probs in cur_prob:
        for ind, prob in enumerate(probs):
            if len(next_prob) < len(probs):
                next_prob.append(prob)
            else:
                next_prob[ind] = next_prob[ind] + prob

    for ind, prob in enumerate(next_prob):
        next_prob[ind] = prob/len(cur_prob)
        
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
    return next_prob

def cycle_events(prev_events, n_event, win_size):
    if len(prev_events) < win_size:
        prev_events.append(n_event)
    else:
        prev_events.pop(0)
        prev_events.append(n_event)
    return prev_events

def calc_event_list(prob_list, row_num, win_size):
    base_prob = initiate_beginning_probs(len(prob_list.keys()))
    next_prob = deepcopy(base_prob)
    event_arr = []
    prev_events = []
    
    for r in range(row_num):
        n_event = calc_next_event(prob_list, next_prob)
        event_arr.append(n_event[0])
        prev_events = cycle_events(prev_events,n_event,win_size)
        next_prob = calc_next_prob(prob_list, n_event, base_prob, prev_events)
    
    return event_arr

def poisson_dist(rate:int, size:int) -> list: return random.poisson(rate, size)

def create_time_serie(period):
    dt = pd.date_range(datetime.today().strftime('%Y-%m-%d'), periods=period, freq="H")
    return pd.date_range(datetime.today().strftime('%Y-%m-%d'), periods=period, freq="H")

def combine_time_event(e_list, tdf):
    return pd.DataFrame({'time_set': tdf, 'events': e_list}, columns=['time_set', 'events'])

def generate_rows(prob_list, period, win_size):
    e_list = calc_event_list(prob_list, period, win_size)
    tdf = create_time_serie(period)
    return combine_time_event(e_list, tdf)

def create_csv(df:DataFrame,path:str): 
    df.to_csv(path)

def initiate_generation(output_path, events = {'a': [['a',0],['b',0.5],['c',0]],
                                  'b': [['a',0],['b',0],['c',0.5]],
                                  'c': [['a',0.5],['b',0],['c',0]]}, years = 1, win_size = 5):
    period = years * 365 * 24
    df = generate_rows(events,period,win_size)
    create_csv(df,output_path)

def run():
    pass

if __name__ == '__main__':
    initiate_generation('test.csv')
    # l_lst = label_gen(3)
    # e_dict = cause_gen(3,l_lst)
    # prob_d = prob_dist(3,l_lst,e_dict,0.3)
    # print(prob_d)
    # generate_rows(prob_d,10,5)
    # path = "output_csv"
    # create_csv(l_lst,horizon(),path)
    # create_time_serie(1)
