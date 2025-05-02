import streamlit as st
import pandas as pd
import logging as lg
from core.data_ingestor import DataIngestor
from core.data_validating import DataValidator
from core.table_joining import DataJoiner
from core.feature_engineering import FeatureEngineer
from core.report_metdata import MetadataExtractor
from core.database_mangement import Manager
from core.logging import get_logger

# ============================
# 1. Logging Setup
# ============================
lg = get_logger(__name__)

# ============================
# 2. Frontend Functionality
# ============================
st.title("DPDZero DataOps Assignment")
uploaders = st.file_uploader("Dump your CSV's", accept_multiple_files=True)
agent = logs = summary = None
if st.button("Submit", type="primary"):
    for uploads in uploaders:
        if uploads.name ==  "agent_roster.csv":
            agent = uploads
        elif uploads.name == "call_logs.csv":
            logs = uploads
        elif uploads.name == "disposition_summary.csv":
            summary = uploads
        else:
            lg.error("uploaded unnecessary files")

    # ============================
    # 2.1 Ingesting
    # ============================
    try:
        if agent:
           ingestor = DataIngestor(logs, summary, agent)
        else:   
            ingestor = DataIngestor(logs, summary)
        try:
            df_call, df_agent, df_summary = ingestor.load_data()
        except Exception as e:
            st.error(f"Error: {e}")
            lg.critical("agent_roster.csv is not in our database neither you have uploaded")
    except Exception as e:
        st.error(f"Error: {e}")
        lg.critical("missing call_logs.csv or disposition_summary.csv")

    # ============================
    # 2.2 Validating
    # ============================
    to_validate_tables = [(df_agent, "agent_roster"), (df_call, "call_logs"), (df_summary, "disposition_summary")]
    validated = []
    for idx, (table, name) in enumerate(to_validate_tables):
        validated.append(DataValidator(table, name))
        validated[idx].concat()
        validated[idx].drop_na()
        validated[idx].drop_duplicates()
        validated[idx].save_data()

    # ============================
    # 2.3 Joining
    # ============================
    joiner = DataJoiner().join()

    # ============================
    # 2.4 Feature Engineering
    # ============================
    features = FeatureEngineer()
    features.total_call_calculator()
    features.unique_loan_calculator()
    features.completed_call_counter()
    features.completed_rate_calculator()
    features.average_call_calculator()
    features.presence_checker()
    features.saving()

    # ============================
    # 2.5 Reporting
    # ============================
    metadata = MetadataExtractor()
    date, rate, active_agents, avg_duration, name = metadata.extractor()

    st.markdown("---")
    st.title(f"Summary for {date}")
    st.metric(label="Top Performer", value=name, delta=f"{rate}% connect rate", border=True)
    col1, col2 = st.columns(2)
    with col1: 
        st.metric(label="Active Agents", value=active_agents, border=True)
    with col2: 
        st.metric(label="Avg Duration (min)", value=avg_duration, border=True)
    st.markdown("---")

    # ============================
    # 2.6 Initiating Storage and Inserting
    # ============================
    sql = Manager()
    sql.insert(date, name, rate, active_agents, avg_duration)

    # ============================
    # 2.7 Leaderboard
    # ============================
    st.title(f"LeaderBoard")
    leaderboard = sql.fetch_topper()
    for i in range(len(leaderboard)):
        st.metric(label= f"Rank {i+1}", value=f"{leaderboard[i][0]}", delta=f"{leaderboard[i][1]}% connect rate", border=True)
    st.markdown("---")

    # ============================
    # 2.8 Graph
    # ============================
    st.title("Day vs Connect Rate")
    day, rate = [], []
    for name, rate_val, day_val in leaderboard:
        day.append(day_val)
        rate.append(float(rate_val))

    chart_data = pd.DataFrame({'rate': rate}, index=day)
    st.line_chart(chart_data)
    lg.info("plotted the graph day vs rate")
    st.markdown("---")

    # ============================
    # 2.9 Output
    # ============================
    st.title("Requested Output")
    df = pd.read_csv("../dpdzero_task/dataset/output/agent_performance_summary.csv")
    st.dataframe(df)
    lg.info("displayed the requested output")
    st.markdown("---")
    st.caption("Created by Ankush for DPDzero Assignment")
    st.caption("+91-7259120176")
    st.caption("ankushpgowda06@gmail.com")










        

