import pandas as pd
import numpy as np
from core.logging import get_logger

# ============================
# 1. Logging Setup
# ============================
lg = get_logger(__name__)


# ============================
# 2. Feature Engineering Class
# ============================
class FeatureEngineer():
    def __init__(self):
        self.df = pd.read_csv("../dpdzero_task/dataset/final_join.csv")
        lg.info("starting the features engineer")

    def total_call_calculator(self):
        self.df['total_call_made'] = self.df.groupby(['agent_id', 'call_date'])['call_id'].transform('count')
        lg.info("calculated total calls made by each agent")

    def unique_loan_calculator(self):
        self.df['unique_loan'] = self.df.groupby(['agent_id', 'call_date'])['installment_id'].transform(lambda x: x.nunique())
        lg.info("calculated total unique loans each agent attended")

    def completed_call_counter(self):
        self.df['complete_call_count'] = self.df[self.df['status'] == 'completed'].groupby(['agent_id', 'call_date'])["status"].transform('count')
        lg.info("calculated total completed calls by each agent")

    def completed_rate_calculator(self):
        self.df['complete_rate'] = self.df.apply(lambda row: (row['complete_call_count'] / row['total_call_made'] if row['complete_call_count'] > 0 else 0), axis=1)
        lg.info("calculated completed calls rate for each agent")

    def average_call_calculator(self):
        self.df['average_call'] = self.df.groupby(['agent_id', 'call_date'])['duration'].transform('mean').round(1)
        lg.info("calculated average time spent on calls for each agent")

    def presence_checker(self):
        self.df["is_present"] = [1 if self.df["login_time"].iloc[i] is not np.nan else 0 for i in range(len(self.df))]
        lg.info("checking agents attendance")

    def saving(self):
        self.df.to_csv("../dpdzero_task/dataset/output/agent_performance_summary.csv", index=False)
        lg.info("storing the agent performance summary csv inside output folder which is in dataset folder")



