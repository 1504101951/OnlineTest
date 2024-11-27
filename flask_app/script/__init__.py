import logging
import os
import traceback
from datetime import datetime, timedelta
from configs.config import BASE_DIR


def clean_temp_file():
    dir_path = f"{BASE_DIR}/temp"
    day_begin = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    for file_name in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file_name)
        if os.path.isfile(file_path):
            creation_time = os.path.getctime(file_path)
            readable_time = datetime.fromtimestamp(creation_time)
            if readable_time < day_begin - timedelta(hours=1):
                try:
                    os.remove(file_path)
                except:
                    logging.error(traceback.format_exc())
    return True
