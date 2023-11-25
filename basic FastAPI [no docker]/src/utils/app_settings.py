import os

class get_settings:
    BROKER_URL = os.getenv("BROKER_URL",default='0.0.0.0:6379')
    BROKER_HASH_KEY = os.getenv("BROKER_HASH_KEY",default='result_API_1-1')