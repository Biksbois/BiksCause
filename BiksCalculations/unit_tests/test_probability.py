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


class test_probability(unittest.TestCase):
    def test_n(self):
        ds_obj = init_obj_test(ds_path=_ds_path)
        
        x = 'x'
        u = 'y'
        
        expected = 4
        actual = ds_obj.calc_n(u, x)
        
        self.assertEqual(expected, actual)
    
    def test_d(self):
        ds_obj = init_obj_test(ds_path=_ds_path)
        
        u = 'y'
        
        expected = 14
        actual = ds_obj.calc_d(u)
        
        self.assertEqual(expected, actual)
    
    def test_lambda(self):
        ds_obj = init_obj_test(ds_path=_ds_path)
        
        expected = 7.5
        actual = calc_lambda(15, 2)
        
        self.assertEqual(expected, actual)
    
    def test_count(self):
        ds_obj = init_obj_test(ds_path=_ds_path)
        x_expected = 5
        y_expected = 7
        z_expected = 7
        
        self.assertTrue(x_expected == ds_obj.cause_dict['x'] and 
                        y_expected == ds_obj.cause_dict['y'] and 
                        z_expected == ds_obj.effect_dict['z'])
    
    def test_p_x_cause(self):
        ds_obj = init_obj_test(ds_path=_ds_path)
        expected = 0.2632
        actual = round(ds_obj.calc_cause_prob('x'), 4)
        
        self.assertEqual(expected, actual)
        
    
    def test_p_x_effect(self):
        ds_obj = init_obj_test(ds_path=_ds_path)
        expected = 0.2632
        actual = round(ds_obj.calc_effect_prob('x'), 4)
        
        self.assertEqual(expected, actual)
    
    def test_p_y_effect(self):
        ds_obj = init_obj_test(ds_path=_ds_path)
        expected = 0.3684
        actual = round(ds_obj.calc_effect_prob('y'), 4)
        
        self.assertEqual(expected, actual)
    
    def test_p_y_cause(self):
        ds_obj = init_obj_test(ds_path=_ds_path)
        expected = 0.3684
        actual = round(ds_obj.calc_cause_prob('y'), 4)
        
        self.assertEqual(expected, actual)
    