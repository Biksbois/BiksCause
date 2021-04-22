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

class Test_Date_Window(unittest.TestCase):
    def test_forward_window_3(self):
        ds_obj = init_obj_test_trafic(head_val=6)
        expected = [('scattered clouds', ['broken clouds', 'overcast clouds', 'overcast clouds']),
                    ('broken clouds', ['overcast clouds', 'overcast clouds', 'broken clouds']),
                    ('overcast clouds', ['overcast clouds', 'broken clouds', 'sky is clear'])]
        actual = []
        
        for w in ds_obj.get_window(backwards=False):
            actual.append(w)
        
        self.assertListEqual(expected, actual)

    def test_backwards_window_3(self):
        ds_obj = init_obj_test_trafic(head_val=6)
        expected = [('overcast clouds', ['overcast clouds', 'broken clouds', 'scattered clouds']),
                    ('broken clouds', ['overcast clouds', 'overcast clouds', 'broken clouds']),
                    ('sky is clear', ['broken clouds', 'overcast clouds', 'overcast clouds'])]
        actual = []
        
        for w in ds_obj.get_window():
            actual.append(w)
        
        self.assertListEqual(expected, actual)
    
    def test_forward_window_two_colums_3(self):
        ds_obj = init_obj_test_trafic(effect_column='weather_main', head_val=6)
        expected = [('Clouds', ['broken clouds', 'overcast clouds', 'overcast clouds']),
                    ('Clouds', ['overcast clouds', 'overcast clouds', 'broken clouds']),
                    ('Clouds', ['overcast clouds', 'broken clouds', 'sky is clear'])]
        actual = []
        
        for w in ds_obj.get_window(backwards=False):
            actual.append(w)
        
        self.assertListEqual(expected, actual)

    def test_backwards_window_two_colums_3(self):
        ds_obj = init_obj_test_trafic(effect_column='weather_main', head_val=6)
        expected = [('Clouds', ['overcast clouds', 'broken clouds', 'scattered clouds']),
                    ('Clouds', ['overcast clouds', 'overcast clouds', 'broken clouds']),
                    ('Clear', ['broken clouds', 'overcast clouds', 'overcast clouds'])]
        actual = []
        
        for w in ds_obj.get_window():
            actual.append(w)
        
        self.assertListEqual(expected, actual)
        
    def test_forward_window_4(self):
        ds_obj = init_obj_test_trafic(head_val=6, windows_size = 4)
        expected = [('scattered clouds', ['broken clouds', 'overcast clouds', 'overcast clouds', 'broken clouds']),
                    ('broken clouds', ['overcast clouds', 'overcast clouds', 'broken clouds', 'sky is clear'])]
        actual = []
        
        for w in ds_obj.get_window(backwards=False):
            actual.append(w)
        
        self.assertListEqual(expected, actual)
    
    def test_backwards_window_4(self):
        ds_obj = init_obj_test_trafic(head_val=6, windows_size = 4)
        expected = [('broken clouds', ['overcast clouds' ,'overcast clouds', 'broken clouds', 'scattered clouds']),
                    ('sky is clear', ['broken clouds','overcast clouds', 'overcast clouds', 'broken clouds'])]
        actual = []
        
        for w in ds_obj.get_window():
            actual.append(w)
        
        self.assertListEqual(expected, actual)
        
    def test_forward_window_two_colums_3(self):
        ds_obj = init_obj_test_trafic(effect_column='weather_main', head_val=6, windows_size = 4)
        expected = [('Clouds', ['broken clouds', 'overcast clouds', 'overcast clouds','broken clouds']),
                    ('Clouds', ['overcast clouds', 'overcast clouds', 'broken clouds', 'sky is clear'])]
        actual = []
        
        for w in ds_obj.get_window(backwards=False):
            actual.append(w)
        
        self.assertListEqual(expected, actual)

    def test_backwards_window_two_colums_3(self):
        ds_obj = init_obj_test_trafic(effect_column='weather_main', head_val=6, windows_size = 4)
        expected = [('Clouds', ['overcast clouds', 'overcast clouds', 'broken clouds', 'scattered clouds']),
                    ('Clear', ['broken clouds' ,'overcast clouds', 'overcast clouds', 'broken clouds'])]
        actual = []
        
        for w in ds_obj.get_window():
            actual.append(w)
        
        self.assertListEqual(expected, actual)
