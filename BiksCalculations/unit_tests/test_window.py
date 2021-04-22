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

class test_window(unittest.TestCase):
    def test_get_windows_backwards(self):
        ds_obj = init_obj_test(head_val=6)
        expected = [('y', ['z', 'y', 'x']), ('x' ,['y', 'z', 'y']), ('y', ['x', 'y', 'z'])]
        actual = []
        
        for w in ds_obj.get_window():
            actual.append(w)
        
        self.assertListEqual(expected, actual)
    
    def test_get_windows_forwards(self):
        ds_obj = init_obj_test(head_val=6)
        expected = [('x', ['y', 'z', 'y']), ('y', ['z', 'y', 'x']), ('z', ['y', 'x', 'y'])]
        actual = []
        
        for w in ds_obj.get_window(backwards=False):
            actual.append(w)
        
        self.assertListEqual(expected, actual)
    
    def test_get_windows_backwards_two_columns(self):
        ds_obj = init_obj_test(effect_column='dur_cluster', head_val=6)
        expected = [('c3', ['z', 'y', 'x']), ('c3' ,['y', 'z', 'y']), ('c2', ['x', 'y', 'z'])]
        actual = []
        
        for w in ds_obj.get_window():
            actual.append(w)
        
        self.assertListEqual(expected, actual)
    
    def test_get_windows_forwards_two_columns(self):
        ds_obj = init_obj_test(effect_column='dur_cluster', head_val=6)
        expected = [('c1', ['y', 'z', 'y']), ('c1', ['z', 'y', 'x']), ('c2', ['y', 'x', 'y'])]
        actual = []
        
        for w in ds_obj.get_window(backwards=False):
            actual.append(w)
        
        self.assertListEqual(expected, actual)
    
    def test_nec(self):
        ds_obj = init_obj_test()
        
        expected = 0.2105
        actual = round(ds_obj.calc_nec('x', 'y'), 4)
        
        self.assertEqual(expected, actual)
    
    def test_suf(self):
        ds_obj = init_obj_test()
        
        expected = 0.1579
        actual = round(ds_obj.calc_suf('x', 'y'), 4)
        
        self.assertEqual(expected, actual)
