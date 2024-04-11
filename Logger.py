import os
import logging
from datetime import datetime
import math

class Logger:
    def __init__(self, log_folder="Log", max_logs=math.inf):
        self.log_folder = log_folder
        self.max_logs = max_logs
        self.log_count = 0

        if not os.path.exists(self.log_folder):
            os.makedirs(self.log_folder)

        log_file = os.path.join(self.log_folder, f"battle_log_{datetime.now().strftime('%Y%m%d%H%M%S')}.log")
        logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def log(self, message):
        if self.log_count < self.max_logs:
            logging.info(message)
            self.log_count += 1

    def close(self):
        logging.shutdown()