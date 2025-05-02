import pandas as pd
from core.logging import get_logger

# ============================
# 1. Logging Setup
# ============================
lg = get_logger(__name__)

# ============================
# 2. Joining Class
# ============================
class DataJoiner:
    def __init__(self):
        lg.info("starting up the joiner to join all 3 tables")
        self.df_agent = pd.read_csv("../dpdzero_task/dataset/agent_roster.csv")
        self.df_call = pd.read_csv("../dpdzero_task/dataset/call_logs.csv")
        self.df_summary = pd.read_csv("../dpdzero_task/dataset/disposition_summary.csv")
        
    def join(self):
        merged = self.df_call.merge(
            self.df_agent,
            on=['agent_id', 'org_id'],
            how='left',
            suffixes=('', '_agent')
    )
        lg.info("joined agent_roster.csv and call_logs.csv into merged")

        final_merged = merged.merge(
            self.df_summary,
            on=['agent_id', 'org_id', 'call_date'],
            how='left',
            suffixes=('', '_disp')
    )
        lg.info("joined merged and disposition_summary into final_join")


        final_merged['call_date'] = pd.to_datetime(final_merged['call_date'], format='mixed')    
        final_merged['login_time'] = pd.to_datetime(final_merged['login_time'], format='mixed').dt.time
        final_merged.to_csv("../dpdzero_task/dataset/final_join.csv", index=False)
        lg.info("saved the final csv inside dataset folder as final_join.csv")
        lg.info("closing the joiner")