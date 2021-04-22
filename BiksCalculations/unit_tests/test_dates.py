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

class test_dates(unittest.TestCase):
    def test_delta_date_hour(self):
        ds_obj = init_obj_test_trafic()
        
        t1 = translate_date('2012-10-02 09:00:00')
        t2 = translate_date('2012-10-02 10:00:00')
        
        actual = calc_deltatime(t1, t2)
        expected = 1
        
        self.assertEqual(actual, expected)
    
    def test_delta_date_days(self):
        ds_obj = init_obj_test_trafic()
        
        t1 = translate_date('2012-10-02 10:00:00')
        t2 = translate_date('2012-10-22 10:00:00')
        
        actual = calc_deltatime(t1, t2)
        expected = 480
        
        self.assertEqual(actual, expected)
    
    def test_delta_date_years(self):
        ds_obj = init_obj_test_trafic()
        
        t1 = translate_date('2012-10-02 10:00:00')
        t2 = translate_date('2013-10-02 10:00:00')
        
        actual = calc_deltatime(t1, t2)
        expected = 8760
        
        self.assertEqual(actual, expected)
    
    def test_str_to_datetime(self):
        ds_obj = init_obj_test_trafic()
        expected = datetime.datetime(2012, 10, 2, 9, 0, 0)
        actual = translate_date('2012-10-02 09:00:00')
        self.assertEqual(expected, actual)
