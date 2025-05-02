import pandas as pd
import numpy as np
from core.logging import get_logger

# ============================
# 1. Logging Setup
# ============================
lg = get_logger(__name__)

class MetadataExtractor():
    def __init__(self):
        self.df = pd.read_csv("../dpdzero_task/dataset/output/agent_performance_summary.csv")
        lg.info("starting metadata extractor")

    def extractor(self):

        def top_performer(df):
            df.sort_values(by=["complete_rate", "unique_loan"], ascending=False, inplace = True)
            return (df.iloc[0].users_first_name +"  "+df.iloc[0].users_last_name), (round(df.iloc[0].complete_rate *100,0))

        sort_dates = sorted(self.df["call_date"].unique(), reverse=True)
        date = sort_dates[0]
        lg.info("got date metadata")

        date_wise = self.df[self.df["call_date"] == date]   
        name, rate = top_performer(date_wise)
        lg.info(f"got name and connect_rate metadata of top performer on {date}")

        active_agents = date_wise[date_wise['is_present'] == 1]['agent_id'].nunique()
        lg.info(f"got total_agents present on {date}")
        avg_duration = round(date_wise['average_call'].mean(), 2)
        lg.info(f"got average calls made on {date}")
        lg.info(f"closing metadata extractor")
        return date, rate, active_agents, avg_duration, name



