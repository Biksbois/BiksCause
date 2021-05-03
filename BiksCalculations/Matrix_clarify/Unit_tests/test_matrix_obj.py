import sys, os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
import unittest
from Matrix_obj import *

rs = result_matrix('BiksCalculations\\results\large_ny_traffic_nst_matrix.csv')
class test_dict(unittest.TestCase):
    def test_matrix_value_getter1(self):
        actual = rs.get_Value('Clouds', 'Clouds')
        expected = 1.0
        self.assertEqual(expected, actual)
        
    def test_matrix_value_getter1(self):
        actual = rs.get_Value('Clear', 'Clear')
        expected = 0.99
        self.assertEqual(expected, actual)
        
    def test_matrix_value_getter1(self):
        actual = rs.get_Value('Clouds', 'Clear')
        expected = 1.0
        self.assertEqual(expected, actual)
        
    def test_matrix_value_getter1(self):
        actual = rs.get_Value('Haze', 'Fog')
        expected = 1.11
        self.assertEqual(expected, actual)