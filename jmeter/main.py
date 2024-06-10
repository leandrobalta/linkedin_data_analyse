import pandas as pd
import os

df = pd.read_csv("csv/result_loop.csv", encoding='utf-8')

#count the number of rows
repetitions = df.shape[0]

latency_mean = "{:.2f}".format(df['Latency'].mean())


print("1," + str(repetitions) + "," + latency_mean)