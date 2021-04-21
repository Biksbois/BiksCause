import jenkspy
import pandas as pd

def create_cluster(ds_arr):
    pass



sales = {
    'Total': [1500, 2100, 80, 20, 75, 1100,40, 2, 1]
}
df = pd.DataFrame(sales)
sdf = df.sort_values(by='Total')

breaks = jenkspy.jenks_breaks(df['Total'], nb_class=3)

sdf['cut_jenksv2'] = pd.cut(df['Total'],
                        bins=breaks,
                        labels=['bucket_1', 'bucket_2','bucket_3'],
                        include_lowest=True)

print(sdf)