import pandas as pd

synthea_path = 'input_csv\\conditions.csv'
look_for = "Normal pregnancy"
start_date = 'start'
end_date = 'stop'
column_name = 'description'


if __name__ == '__main__':
    data = pd.read_csv(synthea_path)
    
    allergy_count = 0
    outgrow_count = 0
    
    for index, row in data.iterrows():
        if row[column_name] == look_for:
            allergy_count += 1
            # if not pd.isnull(row[end_date]):
            if data['encounter'][index+1] == data['encounter'][index]:
                outgrow_count += 1
    
    print(f"People who has {look_for}: {allergy_count}")
    print(f"People who misscarried: {outgrow_count}")
    print(f"percent: {outgrow_count/allergy_count}")