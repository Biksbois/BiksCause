from os import remove
import pandas as pd
import datetime

def convert_to_csv(t_df, output_path):
    t_df.to_csv(output_path)

def remove_and_replace(df, t_df):
    refined_df = df.drop(columns=['year','month','day','hour'])
    refined_df['time_set'] = t_df
    return refined_df

def convert_to_datetime(df):
    t_df = pd.to_datetime(df[['year','month','day','hour']])
    return remove_and_replace(df, t_df)

def initialize_datetime_conversion(input_path:str,output_path:str):
    df = pd.read_csv(input_path)
    t_df = convert_to_datetime(df)
    convert_to_csv(t_df, output_path)

if __name__ == '__main__':
    input_path = 'input_csv\BeijingPM20100101_20151231.csv'
    output_path = 'output_csv\Beijing.csv'
    initialize_datetime_conversion(input_path,output_path)