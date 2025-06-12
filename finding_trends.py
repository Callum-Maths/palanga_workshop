import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class FindingTrends():

    def __init__(self):
        self.contract_data = pd.read_parquet('customer_contract_data.parquet') # 2 snapshots for each customer
        usage_data1 = pd.read_parquet('customer_usage_data1.parquet') # usage of each customer
        usage_data2 = pd.read_parquet('customer_usage_data2.parquet') # usage of each customer
        usage_data3 = pd.read_parquet('customer_usage_data3.parquet') # usage of each customer
        usage_data4 = pd.read_parquet('customer_usage_data4.parquet') # usage of each customer
        self.usage_data = pd.concat([usage_data1, usage_data2, usage_data3, usage_data4], ignore_index=True)
        self.vas_recommendation = pd.read_csv('vas_recommendation.csv')

