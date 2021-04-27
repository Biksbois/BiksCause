from BiksCalculations.dataset_object import *

def generate_lookup_dict():
    # dst_obj = init_obj_test()
    dst_obj = init_obj_test_trafic()
    return generate_suf(dst_obj), generate_nec(dst_obj)

def generate_suf(dst_obj):
    nec_dict = {}
    for win in dst_obj.get_window(backwards=False):
    # for win in dst_obj.get_window():
        if win[0] not in nec_dict:
            nec_dict[win[0]] = {}
        count_instances(nec_dict[win[0]], win[1])
    return nec_dict
        

def generate_nec(dst_obj):
    nec_dict = {}
    for win in dst_obj.get_window():
        if win[0] not in nec_dict:
            nec_dict[win[0]] = {}
        count_instances(nec_dict[win[0]], win[1])
    return nec_dict
        
def count_instances(result_dict ,window): 
    window = list(set(window))
    for w in window:
        if w in result_dict:
            result_dict[w] += 1 
        else:
            result_dict[w] = 1
    return result_dict
    