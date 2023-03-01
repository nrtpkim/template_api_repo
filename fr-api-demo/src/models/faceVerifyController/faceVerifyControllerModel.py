from pydantic import BaseModel
from typing import Union



class inferenceModel(BaseModel):
    username : str
    return_img : Union[str, None] = 'False'
    isRecognite : Union[str, None] = 'False'
    img1 : bytes



class imgPairsModel(BaseModel):
    img1: bytes 
    img2: bytes
    img1_name : str
    img2_name : str

