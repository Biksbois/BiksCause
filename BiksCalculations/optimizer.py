from BiksCalculations.dataset_object import *

def generate_lookup_dict(columns, dst_obj):
    # dst_obj = init_obj_test_trafic()
    suf_dict = generate_suf(dst_obj, columns)
    nec_dict, d_dict = generate_nec(dst_obj, columns)
    return suf_dict, nec_dict, d_dict

def generate_suf(dst_obj, columns):
    nec_dict = {}
    for win in dst_obj.get_multiple_window(columns, backwards=False):
        for key in win[0]:
            if key not in nec_dict:
                nec_dict[key] = {}
            count_instances(nec_dict[key], win[1])
    return nec_dict


# def generate_nec(dst_obj, columns):
#     d_dict = {}
#     nec_dict = {}
#     for win in dst_obj.get_window():
#         if win[0] not in nec_dict:
#             nec_dict[win[0]] = {}
#         count_instances(nec_dict[win[0]], win[1], d_dict=d_dict)
#     return nec_dict, d_dict

def generate_nec(dst_obj, columns):
    d_dict = {}
    nec_dict = {}
    calc_d = True
    
    for win in dst_obj.get_multiple_window(columns):
        calc_d = True
        for key in win[0]:
            if key not in nec_dict:
                nec_dict[key] = {}
            count_instances(nec_dict[key], win[1], d_dict=d_dict, calc_d=calc_d)
            calc_d = False
    return nec_dict, d_dict
        
def count_instances(result_dict, window, d_dict = None, calc_d=None): 
    window = list(set(window))
    for w in window:
        if w in result_dict:
            result_dict[w] += 1 
        else:
            result_dict[w] = 1
        
        if calc_d and not d_dict == None:
            if w in d_dict:
                d_dict[w] += 1
            else:
                d_dict[w] = 1
    
    if d_dict == None:
        return result_dict, d_dict
    else:
        return result_dict

def List_spliter(str_list , parts):
    sublist_size = int(len(str_list) / parts)
    remain_list = sublist_size + (len(str_list) % parts)
    i = 0
    while i < len(str_list):
        if remain_list == len(str_list)-i:
            yield str_list[i : remain_list+i]
            break;
        else:
            yield str_list[i : i + sublist_size]
        i += sublist_size