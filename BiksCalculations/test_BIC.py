import unittest
import datetime
from dataset_object import *
from LL import calc_lambda
from NST import *
from CIR import *

class Test_Window(unittest.TestCase):
    def test_get_windows(self):
        ds_obj = init_obj_test(head_val=6)
        expected = [('y', ['x', 'y', 'z']), ('x' ,['y', 'z', 'y']), ('y', ['z', 'y', 'x'])]
        actual = []
        
        for w in ds_obj.get_window():
            actual.append(w)
        
        self.assertListEqual(expected, actual)
    
    def test_get_windows_backwards(self):
        ds_obj = init_obj_test(head_val=6)
        expected = [('x', ['y', 'z', 'y']), ('y', ['z', 'y', 'x']), ('z', ['y', 'x', 'y'])]
        actual = []
        
        for w in ds_obj.get_window(backwards=False):
            actual.append(w)
        
        self.assertListEqual(expected, actual)
    
    def test_get_windows_two_columns(self):
        ds_obj = init_obj_test(effect_column='dur_cluster', head_val=6)
        expected = [('y', ['x', 'y', 'z']), ('x' ,['y', 'z', 'y']), ('y', ['z', 'y', 'x'])]
        actual = []
        
        for w in ds_obj.get_window():
            actual.append(w)
        
        self.assertListEqual(expected, actual)
    
    def test_get_windows_backwards_two_columns(self):
        ds_obj = init_obj_test(cause_column='dur_cluster', head_val=6)
        expected = [('x', ['y', 'z', 'y']), ('y', ['z', 'y', 'x']), ('z', ['y', 'x', 'y'])]
        actual = []
        
        for w in ds_obj.get_window(backwards=False):
            actual.append(w)
        
        self.assertListEqual(expected, actual)
    
    def test_nec(self):
        ds_obj = init_obj_test()
        
        expected = 0.2105
        actual = round(ds_obj.calc_nec('x', 'y'), 4)
        
        self.assertEqual(expected, actual)
    
    def test_suf(self):
        ds_obj = init_obj_test()
        
        expected = 0.1579
        actual = round(ds_obj.calc_suf('x', 'y'), 4)
        
        self.assertEqual(expected, actual)

class Test_Probability(unittest.TestCase):
    def test_n(self):
        ds_obj = init_obj_test()
        
        x = 'x'
        u = 'y'
        
        expected = 4
        actual = ds_obj.calc_n(u, x)
        
        self.assertEqual(expected, actual)
    
    def test_d(self):
        ds_obj = init_obj_test()
        
        u = 'y'
        
        expected = 14
        actual = ds_obj.calc_d(u)
        
        self.assertEqual(expected, actual)
    
    def test_lambda(self):
        ds_obj = init_obj_test()
        
        expected = 7.5
        actual = calc_lambda(15, 2)
        
        self.assertEqual(expected, actual)
    
    def test_count(self):
        ds_obj = init_obj_test()
        x_expected = 5
        y_expected = 7
        z_expected = 7
        
        self.assertTrue(x_expected == ds_obj.col_dict['x'] and 
                        y_expected == ds_obj.col_dict['y'] and 
                        z_expected == ds_obj.col_dict['z'])
    
    def test_p_x(self):
        ds_obj = init_obj_test()
        expected = 0.2632
        actual = round(ds_obj.calc_prob('x'), 4)
        
        self.assertEqual(expected, actual)
    
    def test_p_y(self):
        ds_obj = init_obj_test()
        expected = 0.3684
        actual = round(ds_obj.calc_prob('y'), 4)
        
        self.assertEqual(expected, actual)
    

class Test_NST(unittest.TestCase):
    def test_nst_rhs(self):
        ds_obj = init_obj_test()
        actual = 0.9832
        alpha_val = 0.66
        lambda_val = 0.5
        x = 'x'
        y = 'y'
        
        expected = round(nst_rhs(ds_obj, alpha_val, lambda_val, x, y), 4)
        
        self.assertEqual(expected, actual)
    
    def test_nst_lhs(self):
        ds_obj = init_obj_test()
        actual = 1.2435
        alpha_val = 0.66
        lambda_val = 0.5
        x = 'x'
        y = 'y'
        
        expected = round(nst_lhs(ds_obj, alpha_val, lambda_val, x, y), 4)
        
        self.assertEqual(expected, actual)
    
    def test_nst(self):
        ds_obj = init_obj_test()
        
        expected = 1.2227
        alpha_val = 0.66
        lambda_val = 0.5
        x = 'x'
        y = 'y'
        actual = round(get_nst(ds_obj, alpha_val, lambda_val, x, y), 4)

        self.assertEqual(expected, actual)

class Test_CIR(unittest.TestCase):
    def test_cir_b(self):
        ds_obj = init_obj_test()
        x = 'x'
        y = 'y'
        actual = 1.0857
        expected = round(calc_cir_b(ds_obj, x, y), 4)
        
        self.assertEqual(actual, expected)
    
    def test_cir_c(self):
        ds_obj = init_obj_test()
        x = 'x'
        y = 'y'
        actual = 1.4286
        expected = round(calc_cir_c(ds_obj, x, y), 4)
        
        self.assertEqual(expected, actual)
    
    def test_cir_c_den(self):
        ds_obj = init_obj_test()
        x = 'x'
        y = 'y'
        actual = 0.2
        expected = round(cir_c_den(ds_obj, x, y), 4)
        
        self.assertEqual(expected, actual)
    
    def test_cir_c_den_den(self):
        ds_obj = init_obj_test()
        x = 'x'
        y = 'y'
        actual = 5
        expected = round(cir_c_den_den(ds_obj, x, y), 4)
    
    def test_cir_c_den_nom(self):
        ds_obj = init_obj_test()
        x = 'x'
        y = 'y'
        actual = 1
        expected = round(cir_c_den_nom(ds_obj, x, y), 4)
        
        self.assertEqual(expected, actual)
    
    def test_cir_nom(self):
        ds_obj = init_obj_test()
        x = 'x'
        y = 'y'
        actual = 0.2857
        expected = round(cir_nom(ds_obj, x, y), 4)
        
        self.assertEqual(expected, actual)

class Test_Dates(unittest.TestCase):
    def test_delta_date_hour(self):
        ds_obj = init_obj_test_trafic()
        
        t1 = ds_obj.translate_date('2012-10-02 09:00:00')
        t2 = ds_obj.translate_date('2012-10-02 10:00:00')
        
        actual = ds_obj.calc_deltatime(t1, t2)
        expected = 1
        
        self.assertEqual(actual, expected)
    
    def test_delta_date_hour(self):
        ds_obj = init_obj_test_trafic()
        
        t1 = ds_obj.translate_date('2012-10-02 09:00:00')
        t2 = ds_obj.translate_date('2012-10-02 10:00:00')
        
        actual = ds_obj.calc_deltatime(t1, t2)
        expected = 1
        
        self.assertEqual(actual, expected)
    
    def test_delta_date_days(self):
        ds_obj = init_obj_test_trafic()
        
        t1 = ds_obj.translate_date('2012-10-02 10:00:00')
        t2 = ds_obj.translate_date('2012-10-22 10:00:00')
        
        actual = ds_obj.calc_deltatime(t1, t2)
        expected = 480
        
        self.assertEqual(actual, expected)
    
    def test_delta_date_years(self):
        ds_obj = init_obj_test_trafic()
        
        t1 = ds_obj.translate_date('2012-10-02 10:00:00')
        t2 = ds_obj.translate_date('2013-10-02 10:00:00')
        
        actual = ds_obj.calc_deltatime(t1, t2)
        expected = 8760
        
        self.assertEqual(actual, expected)
    
    def test_str_to_datetime(self):
        ds_obj = init_obj_test_trafic()
        expected = datetime.datetime(2012, 10, 2, 9, 0, 0)
        actual = ds_obj.translate_date('2012-10-02 09:00:00')
        self.assertEqual(expected, actual)

