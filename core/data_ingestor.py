import pandas as pd
import streamlit as st
from core.logging import get_logger

# ============================
# 1. Logging Setup
# ============================
lg = get_logger(__name__)

# ============================
# 2. Ingestion Class
# ============================
class DataIngestor:
    def __init__(self, call_logs_path, disposition_summary_path, agent_roster_path="../dpdzero_task/dataset/agent_roster.csv"):
        self.call_logs_path = call_logs_path
        self.agent_roster_path = agent_roster_path
        self.disposition_summary_path = disposition_summary_path

    def load_data(self):
        lg.info(f"loading all the table using pandas")
        self.call_logs = pd.read_csv(self.call_logs_path, index_col=False)
        self.agent_roster = pd.read_csv(self.agent_roster_path, index_col=False)    
        self.disposition_summary = pd.read_csv(self.disposition_summary_path, index_col=False)
        return self.call_logs, self.agent_roster, self.disposition_summary
    
    