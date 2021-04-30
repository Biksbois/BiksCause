import sys, os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import unittest
import datetime
from optimizer import *
from dataset_object import *
from LL import calc_lambda
from NST import *
from CIR import *

_ds_path = "BiksCalculations/csv/data.csv"
one_columns = ['label']
three_columns = ['label', 'dur_cluster', 'test']

class test_dict(unittest.TestCase):
    def test_calc_dict_nec_win3(self):
        dst_obj = init_obj_test()
        window_size = 3
        expected = {'x':{'x':1 ,'y':4, 'z':4}, 'y':{'x':4, 'y':5 ,'z': 6}, 'z':{'x':5, 'y':5, 'z':3}}
        actual, _ = generate_nec(dst_obj, one_columns)
        self.maxDiff = None
        self.assertDictEqual(expected,actual)
    
    def test_calc_dict_d_win3(self):
        dst_obj = init_obj_test()
        window_size = 3
        expected = {'x':10, 'y':14, 'z':13}
        _, actual = generate_nec(dst_obj, one_columns)
        self.maxDiff = None
        
        self.assertDictEqual(expected,actual)
        
    def test_calc_dict_suf_win3(self):
        dst_obj = init_obj_test()
        window_size = 3
        expected = {'x':{'x':1, 'y': 3, 'z':4}, 'y':{'x':5, 'y':5, 'z':7}, 'z':{'x':4, 'y':5, 'z':2 }}
        actual = generate_suf(dst_obj, one_columns)
        self.maxDiff = None
        
        self.assertDictEqual(expected,actual)
        
    def test_calc_dict_nec_win3_3col(self):
        dst_obj = init_obj_test(head_val=6)
        window_size = 3
        
        expected = {'a': {'a': 1, 'b': 1, 'c': 1, 'c1': 1, 'c2': 1, 'c3': 1, 'y': 1, 'z': 1},
                    'b': {'a': 1, 'b': 1, 'c': 1, 'c2': 1, 'c3': 1, 'x': 1, 'y': 1, 'z': 1},
                    'c': {'a': 1, 'b': 1, 'c1': 1, 'c2': 1, 'x': 1, 'y': 1, 'z': 1},
                    'c2': {'a': 1, 'b': 1, 'c': 1, 'c2': 1, 'c3': 1, 'x': 1, 'y': 1, 'z': 1},
                    'c3': {'a': 2,'b': 2,'c': 1,'c1': 2,'c2': 2,'c3': 1,'x': 1,'y': 2,'z': 2},
                    'x': {'a': 1, 'b': 1, 'c': 1, 'c1': 1, 'c2': 1, 'c3': 1, 'y': 1, 'z': 1},
                    'y': {'a': 2,'b': 2,'c': 1,'c1': 1,'c2': 2,'c3': 1,'x': 2,'y': 2,'z': 2}}

        actual, _ = generate_nec(dst_obj, three_columns)
        self.maxDiff = None
        
        self.assertDictEqual(expected,actual)
    
    def test_calc_dict_d_win3_3col(self):
        dst_obj = init_obj_test()
        window_size = 3
        expected = {'a': 9,'b': 9,'c': 7,'c1': 3,'c2': 14,'c3': 15,'d': 8,'e': 9,'x': 10,'y': 14,'z': 13}

        _, actual = generate_nec(dst_obj, three_columns)
        self.maxDiff = None
        
        self.assertDictEqual(expected,actual)
        
    def test_calc_dict_suf_win3_3col(self):
        dst_obj = init_obj_test(head_val=6)
        window_size = 3

        expected = {'a': {'a': 2, 'b': 2,'c': 2,'c1': 1,'c2': 2,'c3': 2,'x': 1,'y': 2,'z': 2},
                    'b': {'a': 1, 'b': 1, 'c': 1, 'c2': 1, 'c3': 1, 'x': 1, 'y': 1},
                    'c1': {'a': 2,'b': 2,'c': 2,'c1': 1,'c2': 2,'c3': 2,'x': 1,'y': 2,'z': 2},
                    'c2': {'a': 1, 'b': 1, 'c': 1, 'c2': 1, 'c3': 1, 'x': 1, 'y': 1},
                    'x': {'a': 1, 'b': 1, 'c': 1, 'c1': 1, 'c2': 1, 'c3': 1, 'y': 1, 'z': 1},
                    'y': {'a': 1, 'b': 1, 'c': 1, 'c2': 1, 'c3': 1, 'x': 1, 'y': 1, 'z': 1},
                    'z': {'a': 1, 'b': 1, 'c': 1, 'c2': 1, 'c3': 1, 'x': 1, 'y': 1}}
        

        actual = generate_suf(dst_obj, three_columns)
        self.maxDiff = None
        
        self.assertDictEqual(expected,actual)
        
    def test_list_splitter_1(self):
        lst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        expected = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        actual = []
        for l in List_spliter(lst,1):
            actual.extend(l)
        self.assertListEqual(actual, expected)
    
    def test_list_splitter_2(self):
        lst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        expected = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        actual = []
        for l in List_spliter(lst,2):
            actual.extend(l)
        self.assertListEqual(actual, expected)
        
    def test_list_splitter_3(self):
        lst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        expected = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        actual = []
        for l in List_spliter(lst,3):
            actual.extend(l)
        self.assertListEqual(actual, expected)
        
    def test_list_splitter_2_split_1(self):
        lst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        expected = [1, 2, 3, 4, 5]
        actual = []
        for l in List_spliter(lst,2):
            actual.append(l)
        self.assertListEqual(actual[0], expected)
        
    def test_list_splitter_2_split_2(self):
        lst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        expected = [6, 7, 8, 9, 10]
        actual = []
        for l in List_spliter(lst,2):
            actual.append(l)
        self.assertListEqual(actual[1], expected)

    def test_list_splitter_3_split_1(self):
        lst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        expected = [1, 2, 3]
        actual = []
        for l in List_spliter(lst,3):
            actual.append(l)
        self.assertListEqual(actual[0], expected)

    def test_list_splitter_3_split_2(self):
        lst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        expected = [4, 5, 6]
        actual = []
        for l in List_spliter(lst,3):
            actual.append(l)
        self.assertListEqual(actual[1], expected)
        
    def test_list_splitter_3_split_3(self):
        lst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        expected = [7, 8, 9, 10]
        actual = []
        for l in List_spliter(lst,3):
            actual.append(l)
        self.assertListEqual(actual[2], expected)