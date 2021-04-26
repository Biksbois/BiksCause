import pandas as pd
import os.path
from os import path
import sys
import csv

from csv_column_obj import csv_column
from verify_method import verify_names_and_columns

patient = "patients"
careplan = "careplans"
condition = "conditions"

irrelevant_columns = {patient : csv_column('patient', ['first', 'last', 'suffix', 'maiden', 'address', 'passport', 'drivers', 'ssn']),
                    careplan  : csv_column('id' ,['encounter', 'reasoncode', 'code', 'id']),
                    condition : csv_column('patient', ['encounter', 'code'])
                    }

input_csv_path = "input_csv"
output_csv_path = "output_csv"

if __name__ == '__main__':
    list_of_names = [patient, careplan, condition]
    verify_names_and_columns(list_of_names, irrelevant_columns, input_csv_path)
    
    csv_name = careplan
    
    join_with = [patient]
    
    out_csv_name = f"{output_csv_path}/{csv_name}.csv"
    input_csv_name = f"{input_csv_path}/{csv_name}.csv"
    
    output_csv = pd.read_csv(input_csv_name);
    csv_to_join_with = {}
    
    for name in join_with:
        csv_to_join_with[name] = pd.read_csv(f"{input_csv_path}/{name}.csv")
        csv_to_join_with.update(name = csv_to_join_with[name].drop(irrelevant_columns[name].irrelevant_columns, axis='columns', inplace=True))
        output_csv = output_csv.merge(csv_to_join_with[name], on=irrelevant_columns[name].primary_key)
    
    output_csv.to_csv(out_csv_name)
    print(f"SUCCESS: The new file has been saved to: \"{out_csv_name}\"")