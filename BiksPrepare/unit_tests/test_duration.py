import sys, os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import unittest
import datetime
from duration_method import *

def init_data():
    colum = 'sky is clear'
    csv_path = 'BiksPrepare/unit_tests/test_csv'
    c_start = 'start'
    c_end = 'end'
    cluster_name = 'cluster'
    
    return colum, csv_path, c_start, c_end, cluster_name

class test_duration(unittest.TestCase):
    
    def test_extract_start_i5(self):
        colum, csv_path, c_start, c_end, cluster_name = init_data()
        i = 5
        j_start = 0
        expected_start = 5
        actual_start, _, _= extract_start_end(colum, csv_path, i, c_start, c_end, cluster_name)

        self.assertEqual(expected_start, actual_start)
    
    def test_extract_end_i5(self):
        colum, csv_path, c_start, c_end, cluster_name = init_data()
        i = 5
        j_start = 0
        
        expected_end = 8
        _, actual_end, _ = extract_start_end(colum, csv_path, i, c_start, c_end, cluster_name)

        self.assertEqual(expected_end, actual_end)
    
    def test_extract_cluster_i5(self):
        colum, csv_path, c_start, c_end, cluster_name = init_data()
        i = 5
        j_start = 0
        
        expected_cluster = 'sky is clear_0'
        _, _, actual_cluster = extract_start_end(colum, csv_path, i, c_start, c_end, cluster_name)

        self.assertEqual(expected_cluster, actual_cluster)
    
    def test_extract_start_i8(self):
        colum, csv_path, c_start, c_end, cluster_name = init_data()
        i = 8
        j_start = 0
        
        expected_start = 5
        actual_start, _, _ = extract_start_end(colum, csv_path, i, c_start, c_end, cluster_name)
        self.assertEqual(expected_start, actual_start)
    
    def test_extract_end_i8(self):
        colum, csv_path, c_start, c_end, cluster_name = init_data()
        i = 8
        j_start = 0
        
        expected_end = 8
        _, actual_end, _= extract_start_end(colum, csv_path, i, c_start, c_end, cluster_name)
        self.assertEqual(expected_end, actual_end)
    
    def test_extract_cluster_i8(self):
        colum, csv_path, c_start, c_end, cluster_name = init_data()
        i = 8
        j_start = 0
        
        expected_cluster = 'sky is clear_0'
        _, _, actual_cluster= extract_start_end(colum, csv_path, i, c_start, c_end, cluster_name)
        self.assertEqual(expected_cluster, actual_cluster)
    
    def test_extract_start_i11(self):
        colum, csv_path, c_start, c_end, cluster_name = init_data()
        i = 11
        j_start = 0
        
        expected_start = 11
        actual_start, _, _ = extract_start_end(colum, csv_path, i, c_start, c_end, cluster_name)
        self.assertEqual(expected_start, actual_start)
    
    def test_extract_end_i11(self):
        colum, csv_path, c_start, c_end, cluster_name = init_data()
        i = 11
        j_start = 0
        
        expected_end = 29
        _, actual_end, _= extract_start_end(colum, csv_path, i, c_start, c_end, cluster_name)
        self.assertEqual(expected_end, actual_end)
    
    def test_extract_cluster_i11(self):
        colum, csv_path, c_start, c_end, cluster_name = init_data()
        i = 11
        j_start = 0
        
        expected_cluster = 'sky is clear_2'
        _, _, actual_cluster= extract_start_end(colum, csv_path, i, c_start, c_end, cluster_name)
        self.assertEqual(expected_cluster, actual_cluster)