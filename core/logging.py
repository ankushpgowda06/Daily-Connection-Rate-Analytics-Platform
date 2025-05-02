import logging


# ============================
# 1. Centralized Logging
# ============================
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s'
)

def get_logger(name=None):
    return logging.getLogger(name)
