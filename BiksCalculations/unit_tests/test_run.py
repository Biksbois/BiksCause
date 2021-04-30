import unittest
import datetime
from BiksCalculations.dataset_object import *
from main import *
import filecmp

def get_results():
    actual_base_path = 'BiksCalculations/test_results/actual'
    expected_base_path = 'BiksCalculations/test_results/expected'
    
    csv_path = 'BiksCalculations/csv/test_ny_trafic.csv'
    
    run_experiments(use_optimizer=False, base_path=actual_base_path, csv_path=csv_path)
    run_experiments(use_optimizer=True, base_path=expected_base_path, csv_path=csv_path)

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