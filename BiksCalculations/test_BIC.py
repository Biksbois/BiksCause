import unittest
from dataset_object import *
from LL import calc_lambda

# ds_obj = dt.init_obj_test(head_val = 5)
# win_expected_3 = [["x","y","z"],["y","z","y"]]
# win_expected_4 = [["x","y","z","y"],["y","z","y","x"]]
# win_actual = []
# for w in ds_obj.get_window(windows_size=4):
#     win_actual.append(w.tolist())
# print(win_actual)
class Test_dataset(unittest.TestCase):
    
    def test_windows_3(self):
        ds_obj_3 = init_obj_test(head_val = 4)
        
        win_expected_3 = [["x","y","z"],["y","z","y"]]
        win_actual = []
        for w in ds_obj_3.get_window(windows_size=3):
            win_actual.append(w.tolist())
        self.assertEqual(win_expected_3, win_actual)
    
    def test_windows_4(self):
        ds_obj_4 = init_obj_test(head_val = 5)

        win_expected_4 = [["x","y","z","y"],["y","z","y","x"]]
        win_actual = []
        
        for w in ds_obj_4.get_window(windows_size=4):
            win_actual.append(w.tolist())
        self.assertEqual(win_expected_4, win_actual)
    
    def test_n(self):
        ds_obj = init_obj_test()
        
        x = 'x'
        u = 'y'
        
        expected = 2
        actual = ds_obj.calc_n(u, x)
        
        self.assertEqual(expected, actual)
    
    def test_d(self):
        ds_obj = init_obj_test()
        
        u = 'y'
        
        expected = 15
        actual = ds_obj.calc_d(u)
        
        self.assertEqual(expected, actual)
    
    def test_lambda(self):
        ds_obj = init_obj_test()
        
        expected = 7.5
        actual = calc_lambda(15, 2)
        
        self.assertEqual(expected, actual)
