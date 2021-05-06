from BiksCalculations.dataset_object import *
from BiksCalculations.optimizer import *
from main_paths import *
from BiksCalculations.CIR import *
import numpy as np


def log_l(set_x, set_u, ds_obj, nec_dict, d_dict): # where x is the set of events, and u is the set of potential parents for x
    for x in set_x:
        for u in set_u:
            lam = cir_nom(ds_obj, x, u, big_dict=nec_dict, d_dict=d_dict)
            d = ds_obj.get_d(u, d_dict=d_dict)
            n = ds_obj.get_n(x, u, big_dict=nec_dict)
            ln_lam = np.log(lam)
            
            ll = - lam * d + n * ln_lam
            print(f"ll(x={x}, u={u}) = (-{round(lam, 2)} * {round(d, 2)} + {round(n, 2)} * ln({round(lam, 2)})) = {round(ll, 2)}")

def find_parents():
    main_path = get_large_traffic()
    
    parent_col = 'traffic_volume_cluster'

    base_cols = ['temp_cluster', 'clouds_all_cluster', parent_col]

    cluster_col_to_look = ['weather_description_cluster'] + base_cols
    no_cluster_col_to_look = ['weather_description'] + base_cols
    
    ds_obj = init_obj_test_trafic(ds_path=main_path, head_val=1000, effect_column=parent_col)
    
    support = 0
    
    parent_vals = ds_obj.extract_x()
    
    print(parent_vals)
    
    _, nec_dict, d_dict = generate_lookup_dict(cluster_col_to_look, ds_obj, support)
    
    for val in parent_vals:
        log_l([val], nec_dict[val].keys(), ds_obj, nec_dict, d_dict)