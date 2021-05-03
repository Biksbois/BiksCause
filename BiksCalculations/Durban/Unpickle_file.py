import pickle
import pandas as pd
import datetime

def translate_date(date):
    return datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S') # 2012-10-02 09:00:00

def pickle_to_dict(path):
    f = open(path, 'rb')  
    p_dict = pickle.load(f)        
    f.close()
    return p_dict

def write_pickle(p_dict, path):
    text = open(path, 'w')
    text.write(str(p_dict))
    text.close()

def calc_deltatime(t1, t2):
    diff = t2-t1
    days, seconds = diff.days, diff.seconds
    hours = days * 24 + seconds // 3600
    return hours

def update_temporal_colume(df, date_index):
    dic = {'date_time':[]}
    first = translate_date(str(df.iloc[:, date_index][0]))

    for date in df.iloc[:, date_index]:
        nval = calc_deltatime(first, translate_date(str(date)))

        dic['date_time'].append(nval)
    df.update(dic)
    return df

def conv_tuple(df, colums):
    col_dict = {}
    dict_num = 1
    for index, row in df.iterrows():
        col_dict[dict_num] = []
        for col in colums:
             col_dict[dict_num].append((row[col[0]],row[col[1]]))
        dict_num += 1
    return col_dict

def open_csv(path):
    df = pd.read_csv(path)
    return df

def remove_columes(df,lst):
    return df.drop(columns=lst)

def Save_csv(path, df):
    df.to_csv(path ,index=False)

def Make_pickle_file(p_dict, fname = 'temp'):
    file_to_write = open(fname, "wb")
    pickle.dump(p_dict, file_to_write)

def loadData():
    f = open('temp', 'rb')   # 'r' for reading; can be omitted
    mydict = pickle.load(f)         # load file content as mydict
    f.close()

    text = open('text.txt', 'w')
    text.write(str(mydict))
        
def conv_pickle_to_text(input_path, output_path):
    p_dict = pickle_to_dict(input_path)
    write_pickle(p_dict, output_path)

def conv_csv_to_pickle(input_path, output_path, col_arr, time_col):
    df = open_csv(input_path)
    temporal_df = update_temporal_colume(df, time_col)
    pickle_dict = conv_tuple(df, col_arr)
    Make_pickle_file(pickle_dict, output_path)

if __name__ == '__main__':
    t_weather_desc = [('date_time', 'traffic_volume_cluster'), ('date_time', 'weather_description')]
    t_weather_clust = [('date_time', 'traffic_volume_cluster'), ('date_time', 'weather_description_cluster')]

    conv_csv_to_pickle('input_csv\Metro_Interstate_Traffic_Volume.csv', 'weather_desc', t_weather_desc, 7)
    conv_csv_to_pickle('input_csv\Metro_Interstate_Traffic_Volume.csv', 'weather_clust', t_weather_clust, 7)

    conv_pickle_to_text('weather_desc', 'weather_desc.txt')
    conv_pickle_to_text('weather_clust', 'weather_clust.txt')

# df = open_csv('input_csv\Metro_Interstate_Traffic_Volume.csv')

# common_columns = ['holiday','rain_1h','snow_1h','clouds_all','weather_main','temp','temp_cluster','clouds_all_cluster']
# dev_columns = ['weather_description', 'weather_description_cluster']

# df_weather_desc = remove_columes(df,common_columns)
# df_without_desc = remove_columes(df,common_columns)

# df_without_desc = remove_columes(df_without_desc, dev_columns)

# df = update_temporal_colume(df, 7)

# weather_dict_cluster = conv_tuple(df, [('date_time', 'traffic_volume_cluster'), ('date_time', 'weather_description')])
# weather_dict_description = conv_tuple(df, [('date_time', 'traffic_volume_cluster'), ('date_time', 'weather_description_cluster')])

# Make_pickle_file(weather_dict_cluster, 'mitv_desc')
# Make_pickle_file(weather_dict_description, 'mitv_non_desc')

# loadData()

#Make_pickle_file(dic, path)
# db = loadData()
# f = open("mimic.txt", "a")
# f.write(str(db))
# f.close()