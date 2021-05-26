import unittest
from BiksCalculations.find_ideal_window import find_idea_window

class dist_to_parents(unittest.TestCase):
    def test_dist_to_parents_ten(self):
        actual = find_idea_window('traffic_volume_cluster', 10, 'weather_description_cluster', 'temp_cluster')
        
        expected = {
            'traffic_volume_2': {
                    'scattered clouds_0':[1],
                    'broken clouds_0':[1,1],
                    'overcast clouds_0':[1,1],
                    'sky is clear_0':[1,1,1],
                    'few clouds_1':[1],
                    'temp_5':[1,1,1,1],
                    'temp_6':[1,1,1,1,1]
            }
        }
        
        self.maxDiff = None
        self.assertDictEqual(actual, expected)
    
    def test_dist_to_parents_twenty(self):
        actual = find_idea_window('traffic_volume_cluster', 20, 'weather_description_cluster', 'temp_cluster')
        
        expected = {
            'traffic_volume_0': {
                'scattered clouds_0':[13],
                'broken clouds_0':[9],
                'overcast clouds_0':[10],
                'sky is clear_0':[1,1,1,1,1,1,1],
                'few clouds_1':[3],
                'temp_5':[1, 1, 1],
                'temp_6':[3],
                'temp_4':[1,1,1,1]
            },
            'traffic_volume_1': {
                'scattered clouds_0':[10],
                'broken clouds_0':[6],
                'overcast clouds_0':[7],
                'sky is clear_0':[3,1],
                'few clouds_1':[1,1],
                'temp_5':[7,1],
                'temp_6':[1,1]
            },
            'traffic_volume_2': {
                'scattered clouds_0':[1],
                'broken clouds_0':[1,1],
                'overcast clouds_0':[1,1],
                'sky is clear_0':[1,1,1],
                'few clouds_1':[1],
                'temp_5':[1,1,1,1],
                'temp_6':[1,1,1,1,1]
            },
        }
        
        self.maxDiff = None
        self.assertDictEqual(actual, expected)
