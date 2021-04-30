import pickle
import pandas as pd
import datetime

def translate_date(date):
    return datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S') # 2012-10-02 09:00:00

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

def open_csv(path):
    df = pd.read_csv(path)
    return df

def remove_columes(df,lst):
    return df.drop(columns=lst)

def Save_csv(path, df):
    df.to_csv(path ,index=False)

def Make_pickle_file(dic, path):
    file_to_write = open("output.pickle", "wb")
    pickle.dump(a_dictionary, file_to_write)

def loadData():
    pass
    # for reading also binary mode is important
    # dbfile = open('mimic', 'rb')     
    # db = pickle.load(dbfile)
    # print(db)
    # dbfile.close()
    # return db

df = open_csv('Metro_Interstate_Traffic_Volume.csv')
df = remove_columes(df,['holiday','rain_1h','snow_1h','clouds_all','weather_main','temp'])
df = remove_columes(df,['weather_description'])
df = update_temporal_colume(df,0)

Save_csv('Metro_Interstate_Traffic_Volume_SHORT.csv', df)



#Make_pickle_file(dic, path)
# db = loadData()
# f = open("mimic.txt", "a")
# f.write(str(db))
# f.close()