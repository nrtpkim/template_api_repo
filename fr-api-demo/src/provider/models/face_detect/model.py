import cv2
import sys
import numpy as np
import datetime
import os
import glob
from .retinaface import RetinaFace
import logging

class Detetor:

    def __init__(self, path, gpuid=-1, thresh=0.8, scales=[1.0], count=1):
        self.gpuid = gpuid
        self.thresh = thresh
        self.scales = scales
        self.count = count
        self.path = path

        self.detector = self.__create_model(self.path, self.gpuid)

    def __create_model(self, path, gpuid):
        return RetinaFace(path, 0, gpuid, 'net3')

    def __preprocess(self, img):
        img_shape = img.shape
        target_size = self.scales[0]
        max_size = self.scales[1]
        im_size_min = np.min(img_shape[0:2])
        im_size_max = np.max(img_shape[0:2])

        im_scale = float(target_size) / float(im_size_min)

        # prevent bigger axis from being more than max_size:
        if np.round(im_scale * im_size_max) > max_size:
            im_scale = float(max_size) / float(im_size_max)
        
        return [im_scale]

    def detect(self, img, flip=False):
        # scales = self.__preprocess(img)
        faces, landmarks = self.detector.detect(img, self.thresh, scales=self.scales, do_flip=flip)
        return faces, landmarks
