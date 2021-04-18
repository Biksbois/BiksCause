import unittest
import dataset_object as dt

ds_obj = dt.init_obj_test(head_val = 5)
win_expected_3 = [["x","y","z"],["y","z","y"]]
win_expected_4 = [["x","y","z","y"],["y","z","y","x"]]
win_actual = []
for w in ds_obj.get_window(windows_size=4):
    win_actual.append(w.tolist())
print(win_actual)
class Test_dataset(unittest.TestCase):
    
    def test_windows_3(self):
        ds_obj_3 = dt.init_obj_test(head_val = 4)
        
        win_expected_3 = [["x","y","z"],["y","z","y"]]
        win_actual = []
        for w in ds_obj.get_window(windows_size=3):
            win_actual.append(w.tolist())
        self.assertEqual(win_expected_3, win_actual)
    
    def test_windows_4(self):
        ds_obj_4 = dt.init_obj_test(head_val = 5)

        win_expected_4 = [["x","y","z","y"],["y","z","y","x"]]
        win_actual = []
        
        for w in ds_obj.get_window(windows_size=4):
            win_actual.append(w.tolist())
        self.assertEqual(win_expected_4, win_actual)
        
