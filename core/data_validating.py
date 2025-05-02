import os
import pandas as pd
from core.logging import get_logger
import streamlit as st

# ============================
# 1. Logging Setup
# ============================
lg = get_logger(__name__)

# ============================
# 2. Validation Class
# ============================
class DataValidator:
    file_path = "../dpdzero_task/dataset/"

    def __init__(self, table, name):
        self.df = table
        self.name = name
        lg.info(f"starting the validation for {self.name} table")

    def concat(self):
        if os.path.exists(DataValidator.file_path + self.name + ".csv"):
            lg.info(f"starting to concat old csv with new csv for filename {self.name}")
            old = pd.read_csv(DataValidator.file_path + self.name + ".csv", index_col=False)
            self.df = pd.concat([old, self.df], ignore_index=True)
        lg.info(f"done concating {self.name}")

    
    def drop_na(self):
        priority_column = None
        null_count = self.df.isnull().sum().gt(0).sum()
        if (self.name == "agent_roster") and (null_count > 0):
            lg.info(f"found {null_count} null (column or columns) in {self.name}")
            lg.info(f"starting to drop null values for {self.name}")
            priority_column = ['agent_id', 'org_id']
            try:
                self.df.dropna(subset=priority_column, inplace = True)
                lg.info(f"dropped null rows on columns {priority_column} for {self.name}")
            except Exception as e:
                st.error(f"Error: {e}")
            lg.critical(f"this {self.name} does not contain one of this columns {priority_column}")

        elif (self.name == "call_logs") and (null_count > 0):
            lg.info(f"found {null_count} null (column or columns) in {self.name}")
            lg.info(f"starting to drop null values for {self.name}")
            priority_column = ['agent_id', 'org_id', 'call_id', 'call_date']
            try:
                self.df.dropna(subset=priority_column, inplace = True)
                lg.info(f"dropped null rows on columns {priority_column} for {self.name}")
            except Exception as e:
                st.error(f"Error: {e}")
                lg.critical(f"this {self.name} does not contain one of this columns {priority_column}")

        elif (self.name == "disposition_summarys") and (null_count > 0):
            lg.info(f"found {null_count} null (column or columns) in {self.name}")
            lg.info(f"starting to drop null values for {self.name}")
            priority_column = ['agent_id', 'org_id', 'call_date']
            try:
                self.df.dropna(subset=priority_column, inplace = True)
                lg.info(f"dropped null rows on columns {priority_column} for {self.name}")
            except Exception as e:
                st.error(f"Error: {e}")
                lg.critical(f"this {self.name} does not contain one of this columns {priority_column}")
        else:
            lg.info(f"no null found in {self.name} table")

    def drop_duplicates(self):
        priority_column = None
        if (self.name == "agent_roster"):
            priority_column = ['agent_id']
            lg.info(f"searching for duplicates in column {priority_column} for {self.name} table")
            lg.info(f"found {len(self.df) - self.df[priority_column[0]].nunique()} duplicates in column {priority_column[0]}")
            if (len(self.df) - self.df[priority_column[0]].nunique()) > 0:
                self.df.drop_duplicates(subset=priority_column, inplace = True)
                lg.info("dropped those duplicates")
        
        elif (self.name == "call_logs"):
            priority_column = ['call_id']
            lg.info(f"searching for duplicates in column {priority_column} for {self.name} table")
            lg.info(f"found {len(self.df) - self.df[priority_column[0]].nunique()} duplicates in column {priority_column[0]}")
            if (len(self.df) - self.df[priority_column[0]].nunique()) > 0:
                self.df.drop_duplicates(subset=priority_column, inplace = True)
                lg.info("dropped those duplicates")

        elif (self.name == "disposition_summary"):
            priority_column = ['agent_id', 'call_date']
            lg.info(f"searching for duplicates in column {priority_column} for {self.name} table")
            lg.info(f"found {len(self.df) - self.df[priority_column[0]].nunique()} duplicates in column {priority_column[0]}")
            if (len(self.df) - self.df[priority_column[0]].nunique()) > 0:
                self.df.drop_duplicates(subset=priority_column, inplace = True)
                lg.info("dropped those duplicates")       
        lg.info(f"done validating {self.name} table")

    def save_data(self):
        self.df.to_csv(DataValidator.file_path + self.name + ".csv", index=False)
        lg.info(f"saved the {self.name}.csv inside dataset folder")