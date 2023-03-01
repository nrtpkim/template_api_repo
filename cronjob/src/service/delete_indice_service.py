import logging
from src.provider.ElasticsearchService import ElasticsearchService
import time

logger = logging.getLogger('cronjob')

class DeleteIndeiceService:
    def __init__(self) -> None:
        self.es = ElasticsearchService()

    def delete_indice(self):
        indices_name_arr = self.es.query_index()
        info_register = {}

        for index_name in indices_name_arr:
            ### Query number of register
            result_arr = self.es.query_staff_name(username=index_name)
            no_register_each_index = len(result_arr)
            info_register[index_name] = no_register_each_index


            ### Delete index
            self.es.delete_index(username=index_name)
            logger.info(f"Delete index: {index_name}")
        
        ### log
        if len(indices_name_arr) != 0:
            info_register['summary'] = sum(info_register.values())
            logger.info(f"all infomation: {info_register}")

        # return indices_name_arr

