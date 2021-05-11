from BiksCalculations.dataset_object import *
from BiksCalculations.optimizer import *
from main_paths import *
from BiksCalculations.CIR import *
import numpy as np


def log_l(set_x, set_u, ds_obj, nec_dict, d_dict): # where x is the set of events, and u is the set of potential parents for x
    ll = 0
    
    for x in set_x:
        for u in set_u:
            lam = cir_nom(ds_obj, x, u, big_dict=nec_dict, d_dict=d_dict)
            d = ds_obj.get_d(u, d_dict=d_dict)
            n = ds_obj.get_n(x, u, big_dict=nec_dict)
            
            try:
                ln_lam = np.log(lam)
            except Exception as e:
                ln_lam = 0
                print(e)
            
            # print(f"---\nx = {x}, u = {u}\nlam = {round(lam, 4)}, d = {round(d, 4)}\n n = {round(n, 4)}, ln = {ln_lam}")
            
            
            try:
                ll += - lam * d + n * ln_lam
            except Exception as e:
                ll = 0
                print(e)
            # print(f"ll(x={x}, u={u}) = (-{round(lam, 2)} * {round(d, 2)} + {round(n, 2)} * ln({round(lam, 2)})) = {round(ll, 2)}")
    return ll

def find_parents():
    main_path = get_large_traffic()
    
    parent_col = 'traffic_volume_cluster'

    base_cols = ['temp_cluster', 'clouds_all_cluster', parent_col]

    cluster_col_to_look = ['weather_description_cluster'] + base_cols
    no_cluster_col_to_look = ['weather_description'] + base_cols
    
    ds_obj = init_obj_test_trafic(ds_path=main_path, head_val=50000, effect_column=parent_col, windows_size=2)
    
    support = 0
    
    parent_vals = ds_obj.extract_x()
    
    # print(parent_vals)
    
    _, nec_dict, d_dict = generate_lookup_dict(cluster_col_to_look, ds_obj, support)
    
    
    # for key in nec_dict.keys():
    #     if 'traffic_volume_2' in key:
    #         print(f"{key}")
    #         for key2 in nec_dict[key]:
    #             if 'traffic_volume' in key2:
    #                 print(f"  - {key2}")
    
    set_x_0 = ['traffic_volume_0']
    set_u_0 = ['heavy intensity rain_0', 'mist_0', 'moderate rain_0', 'traffic_volume_0', 'traffic_volume_2']
    
    set_x_1 = ['traffic_volume_1']
    set_u_1 = ['mist_0', 'moderate rain_0', 'traffic_volume_1', 'light rain_0']
    
    set_x_2 = ['traffic_volume_2']
    set_u_2 = ['moderate rain_0', 'light rain_0', 'heavy intensity rain_0', 'traffic_volume_1', 'traffic_volume_2']
    
    ll = 0
    
    ll += log_l(set_x_0, set_u_0, ds_obj, nec_dict, d_dict)
    ll += log_l(set_x_1, set_u_1, ds_obj, nec_dict, d_dict)
    ll += log_l(set_x_2, set_u_2, ds_obj, nec_dict, d_dict)
    
    ln_t = np.log(len(ds_obj.data['temp']))
    paren_len = 0
    
    for lenght in [set_u_0, set_u_1, set_u_2]:
        paren_len += 2 ** len(lenght) #(len(set_u_0) + len(set_u_1) + len(set_u_2))
    
    ds_obj.effect_column = 'traffic_volume_cluster'
    
    n_x = ds_obj.data['traffic_volume_cluster'].value_counts()  
    n_x = n_x['traffic_volume_0']
    
    # n_res = (n_x*(1-np.log(n_x)))/(ln_t)+n_x
    
    # print(f"{n_res} < {2 ** (7)}")
    
    print(f"ll = {ll}, ln(T) = {ln_t}, 2^|U| = {paren_len}")
    print(f"bic = {ll - ln_t * paren_len}")
    
    
    
    # for val in parent_vals:
    #     log_l([val], nec_dict[val].keys(), ds_obj, nec_dict, d_dict)