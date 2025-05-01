from pydantic import BaseModel
from typing import Union


class imgPairsModel(BaseModel):
    img1: bytes 
    img2: bytes
    img1_name : str
    img2_name : str