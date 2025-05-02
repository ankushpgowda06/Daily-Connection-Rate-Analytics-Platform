from core.logging import get_logger
import psycopg2
import os
import numpy as np

# ============================
# 1. Logging Setup
# ============================
lg = get_logger(__name__)

class Manager():
    def __init__(self):
        self.conn = psycopg2.connect(os.environ["DATABASE_URL"])
        lg.info("initiating the connection")

    def insert(self, date, name, rate, active_agents, avg_duration):
        rate = float(rate) if isinstance(rate, np.floating) else rate
        active_agents = int(active_agents) if isinstance(active_agents, np.integer) else active_agents
        avg_duration = float(avg_duration) if isinstance(avg_duration, np.floating) else avg_duration
        with self.conn.cursor() as cur:
            cur.execute("""INSERT INTO agent_performance 
                            (record_date, top_performer, connect_rate, active_agents, avg_duration)
                            VALUES (%s, %s, %s, %s, %s)
                            ON CONFLICT (record_date) DO NOTHING
                        """, (date, name, rate, active_agents, avg_duration))
            self.conn.commit()
        lg.info(f"inserted the topper {name}")

    def fetch_topper(self):
        with self.conn.cursor() as cur:
            cur.execute("""SELECT top_performer, connect_rate, record_date FROM agent_performance ORDER BY connect_rate DESC LIMIT 5""")
            res = cur.fetchall()
            self.conn.commit()
        lg.info(f"app.py requested to fetch all the data")
        return res