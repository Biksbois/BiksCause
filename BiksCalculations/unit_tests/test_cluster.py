import sys, os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import unittest
import datetime
from dataset_object import *
from clustering_method import *

class test_cluster(unittest.TestCase):
    def Test_Create_Cluster(self):
        ds_obj = init_obj_test()
        Test_set = {
        'Test': [4, 5, 9, 10]
        }
        df = create_cluster(Test_set, 'Test')

        col_actual = len(df.columns)
        col_expected = 2

        self.assertEqual(col_actual, col_expected)

    def Test_Apply_Jenks(self):
        pass

    def Test_cl_arr(self):
        pass

    def Test_gvf_score(self):
        pass

    def Test_create_labels(self):
        pass

    




