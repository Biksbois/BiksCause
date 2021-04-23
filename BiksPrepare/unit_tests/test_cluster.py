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
        pass
        #ds_obj = init_obj_test()
        #Test_set = {
        #'Test': [1, 5, 9, 10, 15, 16, 26, 28]
        #}
        #df = create_cluster(Test_set, 'Test')

        #col_actual = len(df.columns)
        #col_expected = 3

        #self.assertEqual(col_actual, col_expected)

    def Test_Apply_Jenks(self):
        ds_obj = init_obj_test()
        Test_set = {
        'Test': [4, 5, 9, 10]
        }
        df = pd.DataFrame(Test_set)
        jdf = apply_jenks(df, 'Test', 2)

        col_actual = len(jdf.columns)
        col_expected = 2

        self.assertEqual(col_actual, col_expected)

    def Test_cl_arr(self):
        ds_obj = init_obj_test()
        Test_set = {
        'Test': [4, 5, 9, 10]
        }
        df = pd.DataFrame(Test_set)
        jdf = apply_jenks(df, 'Test', 2)

        cl_arr = create_cl_arrays(df, 'Test')
        
        arr_actual = len(cl_arr)
        arr_expected = 2

        self.assertEqual(arr_actual,arr_expected)

    def Test_gvf_score(self):
        ds_obj = init_obj_test()
        Test_set_1 = {
        'Test': [4, 5, 9, 10]
        }
        Test_set_2 = {
        'Test': [1, 5, 9, 10, 15, 16, 26, 28]
        }
        col_name = 'Test'

        df1 = pd.DataFrame(Test_set_1)
        df2 = pd.DataFrame(Test_set_2)

        jdf1['Clusters'] = apply_jenks(df, col_name, 2)
        jdf2['Clusters'] = apply_jenks(df2, col_name, 2)
        jdf3['Clusters'] = apply_jenks(df2, col_name, 3)

        ds_arr1 = np.asarray(jdf1[col_name])
        ds_arr2 = np.asarray(jdf2[col_name])
        ds_arr3 = np.asarray(jdf3[col_name])

        cl_arrs1 = create_cl_arrays(jdf1, col_name)
        cl_arrs2 = create_cl_arrays(jdf2, col_name)
        cl_arrs3 = create_cl_arrays(jdf3, col_name)

        gvf1_actual = float("{:.2f}".format(calc_gvf(ds_arr1, cl_arr1))) 
        gvf2_actual = float("{:.2f}".format(calc_gvf(ds_arr2, cl_arr2))) 
        gvf3_actual = float("{:.2f}".format(calc_gvf(ds_arr3, cl_arr3)))

        gvf1_expected = 0.96
        gvf2_expected = 0
        gvf3_expected = 0

        self.assertEqual(gvf1_actual,gvf1_expected)
        
    def Test_create_labels(self):
        arr_labels = create_labels(5)

        arr_len_actual = len(arr_labels)
        arr_len_expected = 5

        self.assertEqual(arr_len_actual, arr_len_expected)

    def Test_one_cluster(self):
        pass

    def Test_two_clusters(self):
        pass

    def Test_duplicates(self):
        pass

    def Test_upper_lower_bound(self):
        pass

    
        

    




