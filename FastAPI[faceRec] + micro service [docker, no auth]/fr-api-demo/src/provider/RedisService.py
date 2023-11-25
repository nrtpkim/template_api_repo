from src.utils.app_settings import get_settings
from typing import Union
from redis import Redis
import logging
import time

class CacheService:
    def __init__(self) -> None:
        print(get_settings().BROKER_URL)
        print(get_settings().BROKER_HASH_KEY)
        self.connection = None
        self.queue_expire_time = 10

        self.__setup()

    def __setup(self, url: str = get_settings().BROKER_URL) -> None:
        '''
        The function creates a Redis connection object and 
        waits for 2 seconds to allow the Redis server to start
        '''
        try:
            logging.info("Setup Redis Broker Connection")
            self.connection = Redis.from_url(f'redis://{url}', retry_on_timeout=True)
            logging.info("Setup Redis Connection")
            return None
        except Exception as e:
            logging.error(
                f"[CacheService] __setup: Cannot connect to Redis server: {e}.")
            time.sleep(2)
            return None
    
    def set_hash(self,  field:str='123test', value: str='QUEUE', key:str=get_settings().BROKER_HASH_KEY,) -> None:
        """
        It sets the hash data into redis.
        
        :param key: The key of the hash
        :type key: str
        :param field: The field of the hash
        :type field: str
        :param value: The value to be set
        :type value: str
        :return: None
        """
        try:
            self.connection.hset(f'{key}', field, value)
            return None
        except Exception as e:
            logging.error(f"[CacheService] set_hash: Cannot set hash data into redis : {e}.")
            return None

    def get_hash(self, field:str, key:str=get_settings().BROKER_HASH_KEY, decode_format:str='utf-8') -> Union[str, None]:
        """
        > This function gets the value of a field in a hash stored at key
        
        :param key: The key of the hash
        :type key: str
        :param field: The field of the hash to get
        :type field: str
        :param decode_format: The format in which the data is to be decoded, defaults to utf-8
        :type decode_format: str (optional)
        :return: A string or None.
        """

        try:
            result = self.connection.hget(f'{key}', field)
            if result is None:
                return None
            
            return result.decode(decode_format)
        except Exception as e:
            logging.error(f"[CacheService] get_hash: Cannot get hash data from redis : {e}.")
            return None
    
    def del_hash(self, field:str, key:str=get_settings().BROKER_HASH_KEY) -> None:
        """
        It deletes a hash from redis.
        
        :param key: The key of the hash
        :type key: str
        :param field: The field to delete from the hash
        :type field: str
        :param prefix: The prefix of the key
        :type prefix: str
        :return: None
        """
        try:
            self.connection.hdel(f'{key}', field)
            return None
        except Exception as e:
            logging.error(f"[CacheService] del_hash: Cannot delete hash from redis : {e}.")
            return None