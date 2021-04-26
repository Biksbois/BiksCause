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

_ds_path = "BiksCalculations/csv/data.csv"

class test_nst(unittest.TestCase):
    def test_nst_rhs(self):
        ds_obj = init_obj_test(ds_path=_ds_path)
        actual = 0.9832
        alpha_val = 0.66
        lambda_val = 0.5
        x = 'x'
        y = 'y'
        
        expected = round(nst_rhs(ds_obj, alpha_val, lambda_val, x, y), 4)
        
        self.assertEqual(expected, actual)
    
    def test_nst_lhs(self):
        ds_obj = init_obj_test(ds_path=_ds_path)
        actual = 1.2435
        alpha_val = 0.66
        lambda_val = 0.5
        x = 'x'
        y = 'y'
        
        expected = round(nst_lhs(ds_obj, alpha_val, lambda_val, x, y), 4)
        
        self.assertEqual(expected, actual)
    
    def test_nst(self):
        ds_obj = init_obj_test(ds_path=_ds_path)
        
        expected = 1.2227
        alpha_val = 0.66
        lambda_val = 0.5
        x = 'x'
        y = 'y'
        actual = round(get_nst(ds_obj, alpha_val, lambda_val, x, y), 4)

        self.assertEqual(expected, actual)
