# this script reads the first 50 rows 

import pandas as pd

df = pd.read_csv('csv/q1.csv', nrows=100)
df.to_csv('q1_test.csv', index=False)

# print(f"Structure file created: test.csv")

# column_list = df.columns.tolist()
# print(column_list)
# print(len(column_list))