# ds_path = u'input_csv\Metro_Interstate_Traffic_Volume.csv'
# # ds_path = u'BiksCalculations\csv\\ny_trafic.csv'
# time_colum = 'date_time'
# temp_csv_path = u'BiksCalculations\csv\\temp_csv'
# col_list = ['weather_main','weather_description','weather_description_cluster'] # 
# cause_column = 'weather_description'
# effect_column = 'weather_description'
# experiment_type = 'small_ny_traffic'
# result_path = 'BiksCalculations/results'

def get_small_traffic():
    return u'input_csv\Metro_Interstate_Traffic_Volume.csv'
    # return u'BiksCalculations\csv\\ny_trafic.csv'

def get_large_traffic():
    return u'input_csv\Metro_Interstate_Traffic_Volume.csv'

def get_trafic_time():
    return 'date_time'

def get_temp_csv_path():
    return u'BiksCalculations\csv\\temp_csv'

def get_cause_effect_col():
    return 'weather_description', 'weather_description'

def get_small_trafic_exp_type():
    return 'small_ny_traffic'

def get_large_trafic_exp_type():
    return 'large_ny_traffic'

def get_result_path():
    return 'BiksCalculations/results'

