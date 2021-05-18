import csv
import statistics
import numpy as np
import os

class box_plotter():
    def __init__(self, path, name = ""):
        self.path = path
        self.name = name
        self.raw_vals = self.open_file()
        self.avg = self.calc_avg()
        self.min,self.max =self.min_max()
        self.median = self.get_median()
        self.Q1,self.Q3 =  self.get_q1_to_q3()
        
    def open_file(self):
        X_new = []
        with open(self.path, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                X_new.extend(row)
        return [int(x) for x in X_new]
    
    def calc_avg(self):
        return sum(self.raw_vals)/len(self.raw_vals)
    
    def min_max(self):
        self.raw_vals.sort()
        return self.raw_vals[0], self.raw_vals[-1]
    
    def get_median(self):
        return statistics.median(self.raw_vals)
        
    def get_q1_to_q3(self):
        return np.quantile(self.raw_vals, .25),np.quantile(self.raw_vals, .75)
    
    def pretty_print(self):
        print("_______________________________")
        print(f"The raw values {self.raw_vals}")
        print(f"Max value: {self.max}")
        print(f"Min value: {self.min}")
        print(f"Median: {self.median}")
        print(f"The average score: {self.avg}")
        print(f"Q1: {self.Q1}")
        print(f"Q3: {self.Q3}")
        print("_______________________________")

def save_boxes(boxes, folder_path):
    headers = ["name","max","min","median","Q1","Q3"]
    indexes = [x.name for x in boxes]
    max_vals = [x.max for x in boxes]
    min_vals = [x.min for x in boxes]
    medians = [x.median for x in boxes]
    Q1s = [x.Q1 for x in boxes]
    Q3s = [x.Q3 for x in boxes]
    vals = [x.raw_vals for x in boxes]
    rows = []
    for i in range(len(indexes)):
        rows.append(vals[i])
    with open(folder_path+"\\synthetic_results.csv", 'w') as f:
        write = csv.writer(f)
        write.writerows(rows)
    
if __name__ == '__main__':
    boxes = []
    path = "BiksCalculations\synthetic_avg_results"
    save_path = "BiksCalculations\Box_plot_csv_for_Roni"
    for file in os.listdir(path):
        if "k10" in file:
            boxes.append(box_plotter(path+"\\"+file, name = file))
    save_boxes(boxes,save_path)