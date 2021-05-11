import unittest
import filecmp
import pandas as pd
from pandas.util.testing import assert_frame_equal

from calc_main import *

# class test_matrix(unittest.TestCase):
#     def test_create_matrix(self):
#         distinct_values = ['a', 'b', 'c', 'd', 'e']
#         actual_path = 'BiksCalculations\\test_results\\actual_matrix.csv'
#         expected_path = 'BiksCalculations\\test_results\\expected_matrix.csv'
        
#         actual_matrix = create_datafram_matric(distinct_values, actual_path)
#         actual_matrix.to_csv(actual_path)
        
#         expected_matric = pd.read_csv(expected_path)
#         actual_matrix = pd.read_csv(actual_path)

#         assert_frame_equal(actual_matrix, expected_matric)
    
#     def test_Construct_Result_Table(self):
#         df_01 = pd.read_csv('BiksCalculations\\test_results\\input_dts_01.csv', index_col=0)
#         df_02 = pd.read_csv('BiksCalculations\\test_results\\input_dts_02.csv', index_col=0)
#         df_03 = pd.read_csv('BiksCalculations\\test_results\\input_dts_03.csv', index_col=0)

#         dts = [{'key_1':df_01}, {'key_1':df_02}, {'key_1':df_03}]
#         # dts = [{'key_1':df_01}, {'key_1':df_02}, {'key_1':df_03}]
#         actual_dts = Construct_Result_Table(dts)
#         actual_dts['key_1'].to_csv('BiksCalculations\\test_results\\actual_dts.csv', index=False, header=True)
        
#         actual_dts = pd.read_csv('BiksCalculations\\test_results\\actual_dts.csv', index_col=0)
#         expected_dts = pd.read_csv('BiksCalculations\\test_results\\expected_dts.csv', index_col=0)
        
#         assert_frame_equal(expected_dts, actual_dts)
    
#     def test_sum(self):
#         l = ['', '']
        
#         self.assertEqual(sum([0 if i == '' else i for i in l]), 0)