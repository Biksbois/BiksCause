import sys, os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import unittest
import datetime
from dataset_object import *
from clustering_method import *

class test_cluster(unittest.TestCase):
    def test_create_cluster(self):
        ds_obj = init_obj_test()
        Test_set = {
        'Test': [4, 5, 9, 10]
        }
        df = create_cluster(Test_set, 'Test')

        col_actual = len(df.columns)
        col_expected = 2

        self.assertEqual(col_actual, col_expected)

    def test_apply_jenks(self):
        pass

    def test_cl_arr(self):
        pass

    def test_gvf_score(self):
        pass

    def test_create_labels(self):
        pass

    




