


class Agent:
    def __init__(self,detection_score=0.4):
        
        self.face_detect_gpuid = -1
        self.face_embedding_gpuid = -1
      
        self.__setup_model(detection_score)

    def __setup_model(self,detection_score):
        pass

    def run(self, text):
        return f"hello : {text}"