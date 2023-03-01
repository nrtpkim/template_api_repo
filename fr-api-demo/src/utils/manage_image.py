import cv2
import io
from PIL import Image
import numpy as np
import base64

def read_image(img_path="assets/photo/unnamed.jpg"):

    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img

def read_img_from_bytes(bytes):
    image = Image.open(io.BytesIO(bytes))
    image_np = np.array(image)

    return image_np

def convert_np_2_base64(frame: np.array, encoding='utf-8', format='.png') -> str:
    _, buffer = cv2.imencode(format, frame)
    frame_base64 = base64.b64encode(buffer).decode(encoding)
    return frame_base64