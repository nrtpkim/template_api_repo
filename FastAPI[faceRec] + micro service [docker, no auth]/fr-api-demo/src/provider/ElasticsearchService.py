import yaml
import time
from elasticsearch import Elasticsearch
from src.utils.app_settings import get_settings
import logging

index_default = 'test009'
logger = logging.getLogger('AI_Service')

class ElasticsearchService:
    def __init__(self) -> None:

        print(get_settings().ELASTIC_ENDPOINT)
        print(get_settings().ELASTIC_PASSWORD)

        self.es = Elasticsearch(
                hosts=[get_settings().ELASTIC_ENDPOINT],
                http_auth=(get_settings().ELASTIC_USERNAME, get_settings().ELASTIC_PASSWORD),
            )
    
    def check_index(self, username):
        return self.es.indices.exists(index=username)
            
    def create_index(self, username):
        if not self.es.indices.exists(index=username):
            payload = {
                    "mappings": {
                    "properties": {
                    "embedding_list":{
                    "type": "dense_vector",
                    "dims": 128
                    }
                    }
                    }}
            res = self.es.indices.create(index=username, body=payload)
            return res
        return f'already have index name : {username}'

    def delete_index(self, username):
        if self.es.indices.exists(index=username):
            res = self.es.indices.delete(index=username, ignore=[400, 404])
            return res
        return f'not have index name : {username}'

    def register(self, staff_name, embeddings_dict, username=index_default):
        '''
            if not index in elastic, system will create index before put embeded to index
        '''
        try:
            if not self.es.indices.exists(index=username): # check index have on elasticsearch
                res = self.create_index(username) # if not have create first
                if res['acknowledged']: 
                    print("Index created successfully")
                else:
                    return "Error creating index"

            # prepare payload put to elastic
            idd = staff_name + '_' + username
            doc = {'id': idd, 
                        'staff_code': staff_name, 
                        'username' : username,
                        'time_stamp' : time.time(),
                        'embedding_list': embeddings_dict["img1"][0].tolist()
                        }

            # put data to Elasticsearch
            res = self.es.index(index=username, id=idd, body=doc)
            return res
                
        except Exception as e:
            logger.error('[face_register] regist face to es: {}'.format(e))
        
    def delete_staff(self, staff_name, username=index_default):
        try:
            if self.es.indices.exists(index=username):
                res = self.es.delete(index=username, id=staff_name + '_' + username)
                return res

            return f'not have index name : {username}'

        except Exception as e:
            logger.error('[delete_staff] regist face to es: {}'.format(e))

    def search_staff(self, embeddings, username=index_default):
        try:
            score = -1
            name = "unknown"

            response = self.es.search( 
                    index=username, 
                    body={ 
                        "size": 1, 
                        "_source": ["staff_code"], 
                        "query": { 
                            "script_score": { 
                                "query" : { 
                                    "match_all": {} 
                                }, 
                                "script": { 
                                    "source": "cosineSimilarity(params.query_vector, 'embedding_list')", 
                                    "params": { 
                                        "query_vector":embeddings.tolist()
                                    } 
                                } 
                            } 
                        } 
                    } 
                )
                
            for hit in response['hits']['hits']: 
                if (float(hit['_score']) > 0.4): 
                    score = hit['_score']
                    name = hit["_source"]["staff_code"]
                else: 
                    score = -1
                    name = "unknown"

            return score, name

        except Exception as e:
            logger.error('[search_staff]: {}'.format(e))

    
    def query_index(self):
        try:
            indices_name_arr = list(self.es.indices.get_alias("*").keys())
            indices_name_arr = [x for x in indices_name_arr if not x.startswith('.')]

            return indices_name_arr
        except Exception as e:
            logger.error('[__query_index]: {}'.format(e))

    def query_staff_name(self, username):
        try:

            result_arr = []
            res = self.es.search(index = username, body={"size": 10000, "query": {"match_all": {}}})

            for idx, hit in enumerate(res['hits']['hits']):
                dict = {
                    'username' : hit["_source"]['username'],
                    'staff_name' : hit["_source"]['staff_code'],
                    'time_stamp' : hit["_source"]['time_stamp']
                    }

                result_arr.append(dict)
            return result_arr
        except Exception as e:
            logger.error('[__query_index]: {}'.format(e))
