from BiksCalculations.dataset_object import *
import itertools

def trim_dict(dict_to_trim, support):
    keys_to_delete = []
    for key in dict_to_trim.keys():
        if dict_to_trim[key] <= support:
            keys_to_delete.append(key)
    
    for key in keys_to_delete:
        del dict_to_trim[key]

    return dict_to_trim

def trim_nested_dict(dict_to_trim, support):
    for key in dict_to_trim:
        dict_to_trim[key] = trim_dict(dict_to_trim[key], support)
    return dict_to_trim

def generate_lookup_dict(columns, dst_obj, support):
    suf_dict = generate_suf(dst_obj, columns)
    nec_dict, d_dict = generate_nec(dst_obj, columns)
    
    suf_dict = trim_nested_dict(suf_dict, support)
    nec_dict = trim_nested_dict(nec_dict, support)
    d_dict = trim_dict(d_dict, support)
    
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
            
            if not dst_obj.hardcoded_cir_m is None:
                count_cir_m_instances(nec_dict[key], win[1], dst_obj.hardcoded_cir_m, d_dict=d_dict, calc_d=calc_d)
            
            calc_d = False
    return nec_dict, d_dict


def derive_unique(hard_code):
    result = []
    
    for key in hard_code.keys():
        result.extend(hard_code[key])
    
    return list(set(result))

def derive_combinations(hard_code):
    unique_indexes = derive_unique(hard_code)
    
    return list(itertools.combinations(unique_indexes, 2))

def get_key(c, extension, index):
    if index == None:
        return (c[0], c[1])
    if index == 1:
        return (c[0], f"{extension}{c[1]}")
    if index == 0:
        return (f"{extension}{c[0]}", c[1])

def handle_dicts(c, d_dict, calc_d, result_dict, extension, index=None):
    key = get_key(c, extension, index)
    
    if not key in result_dict:
        result_dict[key] = 0
    result_dict[key] += 1
    
    if calc_d and not d_dict == None:
        if not key in d_dict:
            d_dict[key] = 0
        d_dict[key] += 1

def count_cir_m_instances(result_dict, window, hard_code, d_dict = None, calc_d=None):
    combi = derive_combinations(hard_code)
    extension = 'not_'
    for c in combi:
        c = sorted(list(c))
        
        if c[0] in window and c[1] in window:
            handle_dicts(c, d_dict, calc_d, result_dict, extension)
        elif c[0] in window and not c[1] in window:
            handle_dicts(c, d_dict, calc_d, result_dict, extension, index=1)
        elif c[1] in window and not c[0] in window:
            handle_dicts(c, d_dict, calc_d, result_dict, extension, index=0)
    
    if d_dict == None:
        return result_dict, d_dict
    else:
        return result_dict

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