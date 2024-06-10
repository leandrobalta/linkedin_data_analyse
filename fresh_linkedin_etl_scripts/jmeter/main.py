import pandas as pd
import os


current_dir = os.path.dirname(__file__)

file_path = os.path.join(current_dir, "csv/result.csv")

df = pd.read_csv(file_path, encoding='utf-8')


# count the number of rows
print(df.shape[0])

# print the mean of the column Latency, formatted to 2 decimal places
print("{:.2f}".format(df['Latency'].mean()))


