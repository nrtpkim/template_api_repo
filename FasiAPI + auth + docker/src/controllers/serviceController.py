from fastapi import APIRouter ,File,  UploadFile, Form, Header, HTTPException
from src.models.serviceControllerModel import imgPairsModel
from PIL import Image
import numpy as np
import io
import time
import datetime


endpoint = APIRouter()

API_KEY = ["AXONS-MOVE"]

def check_timestamp() -> str:
    current_time = time.time() # 1698303714.875011
    current_datetime = datetime.datetime.fromtimestamp(current_time) # 2023-10-26 14:01:54.875011
    timestamp = current_datetime.strftime("%d/%m/%Y %H:%M:%S:%f")[:-3] # 26/10/2023 14:01:54:875
    return timestamp

@endpoint.get("/")
def health_check():
    return {"message" : "API OK", "timestamp" : check_timestamp()}


@endpoint.get("/api-key-auth")
def api_key_auth(val_1, val_2, fromApp: str = Header(...)):
    if fromApp not in API_KEY:
        raise HTTPException(status_code=401, detail=f"Invalid API Key {fromApp}")
    
    return {"message": f"Authenticated with API Key {val_1}, {val_2}"}


@endpoint.post("/image-upload-check")
def image_upload(img1: UploadFile = File(), img2: UploadFile = File(), fromApp: str = Header(...)):
    t = check_timestamp()
    if fromApp not in API_KEY:
        raise HTTPException(status_code=401, detail=f"Invalid API Key {fromApp}")

    
    img1 = img1.file.read()
    img2 = img2.file.read()

    return {"message": f"FINISH len img1: {img1[:10]}, len img2 {img2[:10]}", "timestamp" : t}


@endpoint.post("/image-upload-both")
def image_upload_full(img1: UploadFile = File(), img2: UploadFile = File(), fromApp: str = Header(...)):
    t_in = check_timestamp()
    if fromApp not in API_KEY:
        raise HTTPException(status_code=401, detail=f"Invalid API Key {fromApp}")

    
    img1 = img1.file.read()
    img1 = Image.open(io.BytesIO(img1))
    img1 = np.array(img1)

    img2 = img2.file.read()
    img2 = Image.open(io.BytesIO(img2))
    img2 = np.array(img2)
    
    t_out = check_timestamp()
    res = {
        "message": 
            {
                "img1" : str(img1),
                "img2" : str(img2)
            },
        "timestamp_in" : t_in,
        "timestamp_out" : t_out,
        }

    return res


@endpoint.post("/image-upload-single")
def image_upload_full(img1: UploadFile = File(), fromApp: str = Header(...)):
    t_in = check_timestamp()
    if fromApp not in API_KEY:
        raise HTTPException(status_code=401, detail=f"Invalid API Key {fromApp}")

    
    img1 = img1.file.read()
    img1 = Image.open(io.BytesIO(img1))
    img1 = np.array(img1)


    
    t_out = check_timestamp()
    res = {
        "message": 
            {
                "img1" : str(img1)
            },
        "timestamp_in" : t_in,
        "timestamp_out" : t_out,
        }

    return res