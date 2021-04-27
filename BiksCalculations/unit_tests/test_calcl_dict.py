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

class test_dict(unittest.TestCase):
    def test_calc_dict_nec_win3(self):
        dst_obj = init_obj_test()
        window_size = 3
        expected = {'x':{'x':1 ,'y':4, 'z':4}, 'y':{'x':4, 'y':5 ,'z': 6}, 'z':{'x':5, 'y':5, 'z':3}}
        actual = generate_nec(dst_obj)
        self.assertDictEqual(expected,actual)
        
    def test_calc_dict_suf_win3(self):
        dst_obj = init_obj_test()
        window_size = 3
        expected = {'x':{'x':1, 'y': 3, 'z':4}, 'y':{'x':5, 'y':5, 'z':7}, 'z':{'x':4, 'y':5, 'z':2 }}
        actual = generate_suf(dst_obj)
        self.assertDictEqual(expected,actual)
