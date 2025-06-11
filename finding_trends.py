import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_parquet('part-00000-c0fa7496-921d-48fd-88e8-33ac5109cff7-c000.snappy.parquet')

df_head = df.head(100)
print(df_head)

df_head.to_csv('customer_data_example.csv', index=False)

