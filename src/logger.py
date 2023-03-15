import os
import logging
import sys
from datetime import datetime

LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
logs_path = os.path.join(os.getcwd(),'logs', LOG_FILE)

print(logs_path)
os.makedirs(logs_path, exist_ok=True)

logs_path_file = os.path.join(logs_path, LOG_FILE)
print(logs_path_file)

logging.basicConfig(
    filename = logs_path_file,
    format = "[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level = logging.INFO
)

if __name__ == '__main__':
    print('control here')
    logging.info("Lagging has started")
