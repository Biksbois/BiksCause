from dataset_object import *

# def generate_lookup_dict():
#     dst_obj = init_obj_test()
#     return (generate_suf(dst_obj),generate_nec(dst_obj))

# def generate_suf(dst_obj):
#     for win in dst_obj.get_window(backwards=False):
        

def generate_nec(dst_obj):
    nec_dict = {}
    for win in dst_obj.get_window():
        if win[1] not in nec_dict:
            nec_dict[win[1]] = {}
        count_instances(nec_dict[win[1]], win)
    return nec_dict
        
def count_instances(result_dict ,window): 
    window = list(set(window))
    for w in window[0]:
        if w in result_dict:
            result_dict[w] += 1 
        else:
            result_dict[w] = 1
    return result_dict
    