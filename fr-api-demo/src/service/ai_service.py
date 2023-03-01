
import os
import time
import cv2
import numpy as np
import logging
import time
from elasticsearch import Elasticsearch
from src.provider.models.face_detect.model import RetinaFace
from src.provider.models.face_embedding.model import ArcFace
from src.provider.ElasticsearchService import ElasticsearchService


logger = logging.getLogger('AI_Service')


class Agent():
    def __init__(self,detection_score=0.2):

        self.detection_score = detection_score
        self.face_detect_gpuid = -1
        self.face_embedding_gpuid = -1
        
        self.__setup_es()
        self.__setup_model()
        
    def __setup_es(self):
        try:
            self.es = ElasticsearchService()
            # self.db = MysqlService()
        except Exception as e:
            logger.error('[__setup_es] elasticsearch: {}'.format(e))


    def __setup_model(self):
        try:
            model_path = os.path.join('src','provider','models')
            logger.info(
                'Deploy face detector model on device: ' + str(self.face_detect_gpuid))
            self.face_detector = RetinaFace(os.path.join(model_path, 'face_detect/data/mnet.25'), 0, self.face_detect_gpuid,
                                                'net3')
        
            logger.info(
                'Deploy face embedded model on device: ' + str(self.face_embedding_gpuid))
            self.face_embedding = ArcFace(os.path.join(model_path, 'face_embedding/data/mobilenet/model'),
                                            self.face_embedding_gpuid,
                                            image_size=(112, 112))

        except Exception as e:
            logger.error('[__setup_model] model: {}'.format(e))

    
