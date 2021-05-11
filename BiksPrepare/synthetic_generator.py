import pandas as pd
import numpy as np
from numpy import  random
import os
import random as rand
from string import ascii_lowercase
from copy import deepcopy
import pandas as pd


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
        dict: [Dag, where key is Parent and value is Child]
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

def prob_dist(e_num:int,label_lst:list,e_dict:dict) -> dict:
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
    prob_list = np.ones(e_num)

    # Merge label list with probability distribution
    e_dist_list = [[label_lst[i],prob_list[i]] for i in range(0,len(prob_list))]

    # Assign probability distribution to DAG
    for e in e_dist_list:
        repli_dict[e[0]] = deepcopy(e_dist_list)
    
    # Change Weights according to DAG
    for i in e_dict.keys():
        if repli_dict[i] is not None:
            for ind,j in enumerate(repli_dict[i]):
                if e_dict[i][0] == j[0]:
                    repli_dict[i][ind][1] = 10
    return repli_dict

#Time Horizon
def horizon(ts:int = 0,te:int = 1000,step:int = 60) -> list: return np.arange(ts,te,step)


def yield_prob(e_num:int, w_size:int) -> list:
    total_t = horizon()[-1]
    prob_dict = {}
    event_list = []
    weights = [1,1,1,1,10]
    labels =['a','b','c','d','e']
    for i in range(total_t):
        event_list.append(np.random.choice(labels,weights))
        event_list.append(i)
    return prob_dict

def poisson_dist(rate:int, size:int) -> list: return random.poisson(rate, size)

def create_csv(events:list, time:list, path:str): 
    data_tuples = list(zip(events,time))
    df = pd.DataFrame(data_tuples, columns=['events','time'])
    df.to_csv(path)

def run():
    pass

if __name__ == '__main__':
    l_lst = label_gen(5)
    e_dict = cause_gen(5,l_lst)
    yield_prob(10,20)
    path = "C:\\Users\\ronih\\Documents\\UNI\\project\\BiksCause\\BiksCause\\input_csv\\synthetic\\test.csv"
    create_csv(l_lst,horizon(),path)