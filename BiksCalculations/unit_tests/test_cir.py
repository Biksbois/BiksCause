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

class test_cir(unittest.TestCase):
    def test_cir_b(self):
        ds_obj = init_obj_test(ds_path=_ds_path)
        x = 'x'
        y = 'y'
        actual = 1.0857
        expected = round(calc_cir_b(ds_obj, x, y), 4)
        
        self.assertEqual(actual, expected)
    
    def test_cir_c(self):
        ds_obj = init_obj_test(ds_path=_ds_path)
        x = 'x'
        y = 'y'
        actual = 1.4286
        expected = round(calc_cir_c(ds_obj, x, y), 4)
        
        self.assertEqual(expected, actual)
    
    def test_cir_c_den(self):
        ds_obj = init_obj_test(ds_path=_ds_path)
        x = 'x'
        y = 'y'
        actual = 0.2
        expected = round(cir_c_den(ds_obj, x, y), 4)
        
        self.assertEqual(expected, actual)
    
    def test_cir_c_den_den(self):
        ds_obj = init_obj_test(ds_path=_ds_path)
        x = 'x'
        y = 'y'
        actual = 5
        
        
        expected = round(cir_c_den_den(ds_obj, x, y), 4)
    
    def test_cir_c_den_nom(self):
        ds_obj = init_obj_test(ds_path=_ds_path)
        x = 'x'
        y = 'y'
        actual = 1
        expected = round(cir_c_den_nom(ds_obj, x, y), 4)
        
        self.assertEqual(expected, actual)
    
    def test_cir_nom(self):
        ds_obj = init_obj_test(ds_path=_ds_path)
        x = 'x'
        y = 'y'
        actual = 0.2857
        expected = round(cir_nom(ds_obj, x, y), 4)
        
        self.assertEqual(expected, actual)
    
    def test_get_n(self):
        ds_obj = init_obj_test(ds_path=_ds_path)
        x = 'x'
        y = 'y'
        test_dict = {x:{y:5}}
        actual = get_n(ds_obj, x, y, test_dict)
        expected = 5
        self.assertEqual(actual, expected)
