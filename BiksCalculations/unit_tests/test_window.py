import sys, os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import unittest
import datetime
from dataset_object import *
from LL import calc_lambda
from NST import *
from CIR import *
from BiksCalculations.optimizer import *


_ds_path = "BiksCalculations/csv/data.csv"

class test_window(unittest.TestCase):
    def test_get_windows_backwards(self):
        ds_obj = init_obj_test(head_val=6, ds_path = _ds_path)
        expected = [('y', ['z', 'y', 'x']), ('x' ,['y', 'z', 'y']), ('y', ['x', 'y', 'z'])]
        actual = []
        
        for w in ds_obj.get_window():
            actual.append(w)
        
        self.assertListEqual(expected, actual)
    
    def test_get_windows_forwards(self):
        ds_obj = init_obj_test(head_val=6, ds_path = _ds_path)
        expected = [('x', ['y', 'z', 'y']), ('y', ['z', 'y', 'x']), ('z', ['y', 'x', 'y'])]
        actual = []
        
        for w in ds_obj.get_window(backwards=False):
            actual.append(w)
        
        self.assertListEqual(expected, actual)
    
    def test_get_windows_backwards_two_columns(self):
        ds_obj = init_obj_test(effect_column='dur_cluster', head_val=6 , ds_path = _ds_path)
        expected = [('c3', ['z', 'y', 'x']), ('c3' ,['y', 'z', 'y']), ('c2', ['x', 'y', 'z'])]
        actual = []
        
        for w in ds_obj.get_window():
            actual.append(w)
        
        self.assertListEqual(expected, actual)
    
    def test_get_windows_forwards_two_columns(self):
        ds_obj = init_obj_test(effect_column='dur_cluster', head_val=6, ds_path = _ds_path)
        expected = [('c1', ['y', 'z', 'y']), ('c1', ['z', 'y', 'x']), ('c2', ['y', 'x', 'y'])]
        actual = []
        
        for w in ds_obj.get_window(backwards=False):
            actual.append(w)
        
        self.assertListEqual(expected, actual)
    
    def test_nec(self):
        ds_obj = init_obj_test(ds_path = _ds_path)
        
        expected = 0.2105
        actual = round(ds_obj.calc_nec('x', 'y'), 4)
        
        self.assertEqual(expected, actual)
    
    def test_suf(self):
        ds_obj = init_obj_test(ds_path = _ds_path)
        
        expected = 0.1579
        actual = round(ds_obj.calc_suf('x', 'y'), 4)
        
        self.assertEqual(expected, actual)
    
    def test_get_multiple_windows_backwards(self):
        ds_obj = init_obj_test(head_val=6, ds_path = _ds_path)
        columns = ['label','duration','dur_cluster','test']
        expected = [(['y','55','c3','c'], ['z','38','c2','b','y','19','c1','a','x','2','c1','a']), 
                    (['x','43','c3','a'], ['y','55','c3','c','z','38','c2','b','y','19','c1','a']), 
                    (['y','23','c2','b'], ['x','43','c3','a','y','55','c3','c','z','38','c2','b'])]
        actual = []
        
        for w in ds_obj.get_multiple_window(columns):
            actual.append(w)
        
        self.maxDiff = None
        self.assertListEqual(expected, actual)

    def test_get_multiple_windows_forwards(self):
        ds_obj = init_obj_test(head_val=6, ds_path = _ds_path)
        columns = ['label','duration','dur_cluster','test']
        expected = [(['x','2','c1','a'], ['y', '19', 'c1', 'a', 'z', '38', 'c2', 'b', 'y', '55', 'c3', 'c']), 
                    (['y','19','c1','a'], ['z', '38', 'c2', 'b', 'y', '55', 'c3', 'c', 'x', '43', 'c3', 'a']), 
                    (['z','38','c2','b'], ['y', '55', 'c3', 'c', 'x', '43', 'c3', 'a', 'y', '23', 'c2', 'b'])]
        actual = []
        
        for w in ds_obj.get_multiple_window(columns, backwards=False):
            actual.append(w)
        
        self.maxDiff = None
        self.assertListEqual(expected, actual)
    
    def test_hardcoded_cir_m_nec(self):
        hard_code = {'traffic_volume_2':['scattered clouds_0', 'temp_5', 'traffic_volume_1', 'temp_4'],
                    'traffic_volume_1': ['sky is clear_0', 'temp_6', 'traffic_volume_2', 'temp_4']}

        result_dict = {}
        expected_dict = {
            ('temp_5', 'not_temp_6'): 1, 
            ('temp_5', 'traffic_volume_1'): 1, 
            ('temp_5', 'traffic_volume_2'): 1, 
            ('not_sky is clear_0', 'temp_5'): 1, 
            ('temp_4', 'temp_5'): 1, 
            ('scattered clouds_0', 'temp_5'): 1, 
            ('not_temp_6', 'traffic_volume_1'): 1, 
            ('not_temp_6', 'traffic_volume_2'): 1, 
            ('temp_4', 'not_temp_6'): 1, 
            ('scattered clouds_0', 'not_temp_6'): 1, 
            ('traffic_volume_1', 'traffic_volume_2'): 1, 
            ('not_sky is clear_0', 'traffic_volume_1'): 1, 
            ('temp_4', 'traffic_volume_1'): 1, 
            ('scattered clouds_0', 'traffic_volume_1'): 1, 
            ('not_sky is clear_0', 'traffic_volume_2'): 2, 
            ('temp_4', 'traffic_volume_2'): 2, 
            ('scattered clouds_0', 'traffic_volume_2'): 2, 
            ('not_sky is clear_0', 'temp_4'): 2, 
            ('scattered clouds_0', 'not_sky is clear_0'): 2, 
            ('scattered clouds_0', 'temp_4'): 2, 
            ('not_temp_5', 'temp_6'): 1, 
            ('not_temp_5', 'traffic_volume_2'): 1, 
            ('temp_4', 'not_temp_5'): 1, 
            ('scattered clouds_0', 'not_temp_5'): 1, 
            ('temp_6', 'not_traffic_volume_1'): 1, 
            ('temp_6', 'traffic_volume_2'): 1, 
            ('not_sky is clear_0', 'temp_6'): 1, 
            ('temp_4', 'temp_6'): 1, 
            ('scattered clouds_0', 'temp_6'): 1, 
            ('not_traffic_volume_1', 'traffic_volume_2'): 1, 
            ('temp_4', 'not_traffic_volume_1'): 1, 
            ('scattered clouds_0', 'not_traffic_volume_1'): 1
        }
        
        window_1 = ['traffic_volume_2', 'traffic_volume_1', 'traffic_volume_0', 'temp_5', 'temp_4', 'scattered clouds_0']
        window_2 = ['traffic_volume_2', 'traffic_volume_2', 'traffic_volume_0', 'temp_6', 'temp_4', 'scattered clouds_0']
        
        count_cir_m_instances(result_dict, window_1, hard_code, d_dict = None, calc_d=None)
        count_cir_m_instances(result_dict, window_2, hard_code, d_dict = None, calc_d=None)

        self.maxDiff = None
        
        self.assertDictEqual(result_dict, expected_dict)
        
    def test_hardcoded_cir_m_d(self):
        hard_code = {'traffic_volume_2':['scattered clouds_0', 'temp_5', 'traffic_volume_1', 'temp_4'],
                    'traffic_volume_1': ['sky is clear_0', 'temp_6', 'traffic_volume_2', 'temp_4']}

        result_dict = {}
        # expected_dict = {
        #     ('temp_5', 'traffic_volume_1'):1,
        #     ('traffic_volume_1', 'traffic_volume_2'):1,
        #     ('scattered clouds_0', 'traffic_volume_1'):1,
        #     ('temp_4', 'traffic_volume_1'):1,
        #     ('temp_5', 'traffic_volume_2'):1,
        #     ('scattered clouds_0', 'temp_5'):1,
        #     ('temp_4', 'temp_5'):1,
        #     ('scattered clouds_0', 'traffic_volume_2'):2,
        #     ('temp_4', 'traffic_volume_2'):2,
        #     ('scattered clouds_0', 'temp_4'):2,
        #     ('temp_6', 'traffic_volume_2'):1,
        #     ('scattered clouds_0', 'temp_6'):1,
        #     ('temp_4', 'temp_6'):1
        # }
        
        expected_dict = {
            ('temp_5', 'not_temp_6'): 1, 
            ('temp_5', 'traffic_volume_1'): 1, 
            ('temp_5', 'traffic_volume_2'): 1, 
            ('not_sky is clear_0', 'temp_5'): 1, 
            ('temp_4', 'temp_5'): 1, 
            ('scattered clouds_0', 'temp_5'): 1, 
            ('not_temp_6', 'traffic_volume_1'): 1, 
            ('not_temp_6', 'traffic_volume_2'): 1, 
            ('temp_4', 'not_temp_6'): 1, 
            ('scattered clouds_0', 'not_temp_6'): 1, 
            ('traffic_volume_1', 'traffic_volume_2'): 1, 
            ('not_sky is clear_0', 'traffic_volume_1'): 1, 
            ('temp_4', 'traffic_volume_1'): 1, 
            ('scattered clouds_0', 'traffic_volume_1'): 1, 
            ('not_sky is clear_0', 'traffic_volume_2'): 2, 
            ('temp_4', 'traffic_volume_2'): 2, 
            ('scattered clouds_0', 'traffic_volume_2'): 2, 
            ('not_sky is clear_0', 'temp_4'): 2, 
            ('scattered clouds_0', 'not_sky is clear_0'): 2, 
            ('scattered clouds_0', 'temp_4'): 2, 
            ('not_temp_5', 'temp_6'): 1, 
            ('not_temp_5', 'traffic_volume_2'): 1, 
            ('temp_4', 'not_temp_5'): 1, 
            ('scattered clouds_0', 'not_temp_5'): 1, 
            ('temp_6', 'not_traffic_volume_1'): 1, 
            ('temp_6', 'traffic_volume_2'): 1, 
            ('not_sky is clear_0', 'temp_6'): 1, 
            ('temp_4', 'temp_6'): 1, 
            ('scattered clouds_0', 'temp_6'): 1, 
            ('not_traffic_volume_1', 'traffic_volume_2'): 1, 
            ('temp_4', 'not_traffic_volume_1'): 1, 
            ('scattered clouds_0', 'not_traffic_volume_1'): 1
        }

        
        window_1 = ['traffic_volume_2', 'traffic_volume_1', 'traffic_volume_0', 'temp_5', 'temp_4', 'scattered clouds_0']
        window_2 = ['traffic_volume_2', 'traffic_volume_2', 'traffic_volume_0', 'temp_6', 'temp_4', 'scattered clouds_0']
        
        count_cir_m_instances({}, window_1, hard_code, d_dict = result_dict, calc_d=True)
        count_cir_m_instances({}, window_2, hard_code, d_dict = result_dict, calc_d=True)

        self.maxDiff = None
        
        self.assertDictEqual(result_dict, expected_dict)
    
    def test_hardcoded_cir_m_nec_one_window(self):
        hard_code = {'traffic_volume_2':['scattered clouds_0', 'temp_5', 'traffic_volume_1'],
                    'traffic_volume_1': ['sky is clear_0', 'temp_6', 'traffic_volume_2']}

        result_dict = {}
        expected_dict = {
            ('not_scattered clouds_0', 'traffic_volume_1'):1,
            ('not_scattered clouds_0', 'traffic_volume_2'):1,
            ('not_scattered clouds_0', 'temp_6'):1,
            ('not_temp_5', 'traffic_volume_1'):1,
            ('traffic_volume_1', 'traffic_volume_2'): 1,
            ('not_sky is clear_0', 'traffic_volume_1'):1,
            ('temp_6', 'traffic_volume_1'):1,
            ('not_temp_5', 'traffic_volume_2'):1,
            ('not_temp_5', 'temp_6'):1,
            ('not_sky is clear_0', 'traffic_volume_2'):1,
            ('temp_6', 'traffic_volume_2'):1,
            ('not_sky is clear_0', 'temp_6'):1
        }

        window_1 = ['traffic_volume_2', 'traffic_volume_1', 'traffic_volume_0', 'temp_6']
        
        count_cir_m_instances(result_dict, window_1, hard_code, d_dict = None, calc_d=None)
        
        self.maxDiff = None
        
        self.assertDictEqual(result_dict, expected_dict)
    
    def test_derive_unique(self):
        hard_code = {'traffic_volume_2':['scattered clouds_0', 'temp_5', 'traffic_volume_1'],
                    'traffic_volume_1': ['sky is clear_0', 'temp_6', 'traffic_volume_1']} 
        
        actual = derive_unique(hard_code)
        expected = ['sky is clear_0', 'temp_6', 'traffic_volume_1', 'scattered clouds_0', 'temp_5']

        actual = sorted(actual)
        expected = sorted(expected)

        self.assertListEqual(actual, expected)
