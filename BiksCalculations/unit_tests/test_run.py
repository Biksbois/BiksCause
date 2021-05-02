import unittest
import datetime
from BiksCalculations.dataset_object import *
from main import *
import filecmp
from main_paths import *

def get_results():
    actual_base_path = 'BiksCalculations/test_results/actual'
    expected_base_path = 'BiksCalculations/test_results/expected'
    
    csv_path = 'BiksCalculations/csv/test_ny_trafic.csv'
    
    cause_column, effect_column = get_cause_effect_col()
    col_list = ['weather_main','weather_description']
    
    ds_path = get_small_traffic()
    experiment_type = get_small_trafic_exp_type()
    ds_obj = init_obj_test_trafic(cause_column=cause_column, effect_column=effect_column, ds_path=ds_path)
    
    run_experiments(ds_obj, cause_column, effect_column, ds_path, actual_base_path, col_list, experiment_type, use_optimizer=True)
    run_experiments(ds_obj, cause_column, effect_column, ds_path, expected_base_path, col_list, experiment_type, use_optimizer=False)

class test_run(unittest.TestCase):
    def test_a_cir_b(self):
        get_results()
        
        actual_path = 'BiksCalculations\\test_results\\actual\\ny_traffic_cir_b_matrix.csv'
        expected_path = 'BiksCalculations\\test_results\\expected\\ny_traffic_cir_b_matrix.csv'
        
        self.assertTrue(filecmp.cmp(actual_path, expected_path), 'These two CSV are not at all the same.')
    
    def test_b_cir_c(self):
        actual_path = 'BiksCalculations\\test_results\\actual\\ny_traffic_cir_c_matrix.csv'
        expected_path = 'BiksCalculations\\test_results\\expected\\ny_traffic_cir_c_matrix.csv'
        
        self.assertTrue(filecmp.cmp(actual_path, expected_path), 'These two CSV are not at all the same.')
    
    def test_c_nst(self):
        actual_path = 'BiksCalculations\\test_results\\actual\\ny_traffic_nst_matrix.csv'
        expected_path = 'BiksCalculations\\test_results\\expected\\ny_traffic_nst_matrix.csv'
        
        self.assertTrue(filecmp.cmp(actual_path, expected_path), 'These two CSV are not at all the same.')