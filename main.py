from utils import CassandraMockData
import time
import logging
import sys

logging.basicConfig(level=logging.INFO, handlers=[logging.StreamHandler(sys.stdout)])

data = CassandraMockData()

logging.info("Main    : Starting Application")

data.speed_run_populate_data(core=5)

# start_time = time.time()

# data.populate_mock_data(limit=50001)

# end_time = time.time()

# time_spend = end_time - start_time

# logging.info(f"Main    : Finished Application - Spending {time_spend} to finish")
