# import unittest
# import datetime
# from BiksCalculations.dataset_object import *
# from main import *
# import filecmp
# from main_paths import *

# def get_results():
#     actual_base_path = 'BiksCalculations/test_results/actual'
#     expected_base_path = 'BiksCalculations/test_results/expected'
    
#     csv_path = get_small_traffic()
    
#     cause_column, effect_column = get_cause_effect_col()
#     col_list = ['weather_main','weather_description', 'traffic_volume_cluster']
#     e_obj = exp_obj([0.66], [0.5], 6, 100, 'test', 'large', 0)
    
#     ds_path = get_small_traffic()
#     experiment_type = get_small_trafic_exp_type()
#     # ds_obj = init_obj_test_trafic(cause_column=cause_column, effect_column=effect_column, ds_path=ds_path)
#     ds_obj = init_obj_test_trafic(cause_column=cause_column, effect_column=effect_column, ds_path=ds_path, windows_size=e_obj.window_size, head_val=e_obj.head_val)
    
#     run_experiments(ds_obj, cause_column, effect_column, ds_path, actual_base_path, col_list, col_list, e_obj, [3], use_optimizer=True)
#     run_experiments(ds_obj, cause_column, effect_column, ds_path, expected_base_path, col_list, col_list, e_obj, [3], use_optimizer=False)

# class test_run(unittest.TestCase):
#     def test_a_cir_b(self):
#         get_results()
        
#         actual_path = 'BiksCalculations\\test_results\\actual\\cluster\\test_cir_b_h100_w3_matrix.csv'
#         expected_path = 'BiksCalculations\\test_results\\expected\\cluster\\test_cir_b_h100_w3_matrix.csv'
        
#         actual_df = pd.read_csv(actual_path)
#         actual_df.sort_values(by=['Clouds'], inplace=True)
#         actual_df.reindex(sorted(actual_df.columns), axis=1)
#         actual_df.to_csv(actual_path, index = False, header=True)
        
#         expected_df = pd.read_csv(expected_path)
#         expected_df.sort_values(by=['Clouds'], inplace=True)
#         expected_df.reindex(sorted(expected_df.columns), axis=1)
#         expected_df.to_csv(expected_path, index = False, header=True)
        
#         self.assertTrue(filecmp.cmp(actual_path, expected_path), 'These two CSV are not at all the same.')
    
#     def test_b_cir_c(self):
#         actual_path = 'BiksCalculations\\test_results\\actual\\cluster\\test_cir_c_h100_w3_matrix.csv'
#         expected_path = 'BiksCalculations\\test_results\\expected\\cluster\\test_cir_c_h100_w3_matrix.csv'
        
#         self.assertTrue(filecmp.cmp(actual_path, expected_path), 'These two CSV are not at all the same.')
    
#     def test_c_nst(self):
#         actual_path = 'BiksCalculations\\test_results\\actual\\no_cluster\\test_nst_a66_l5_h100_w3_matrix.csv'
#         expected_path = 'BiksCalculations\\test_results\\expected\\no_cluster\\test_nst_a66_l5_h100_w3_matrix.csv'
        
#         self.assertTrue(filecmp.cmp(actual_path, expected_path), 'These two CSV are not at all the same.')