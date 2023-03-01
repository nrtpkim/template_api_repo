import os
import logging
from datetime import datetime

def create_dir(dir_path):
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)


def log_setting(file_name="all_logs", project_path ='./', logs_tag= 'ai_agent'):
    # Setup logging
    logs_dir = os.path.join(project_path, "logs")
    create_dir(logs_dir)
    logs_file = os.path.join(logs_dir, file_name + "_%s.log"%(datetime.now().strftime("%Y_%m_%d")))
    logger = logging.getLogger(logs_tag)

    
    formatter = logging.Formatter('%(asctime)s | %(levelname)s -> %(message)s')

    file_handler = logging.FileHandler(logs_file)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    # creating a handler to log on the console
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(logging.INFO)
    
    logger.setLevel(logging.DEBUG)
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
    return logger