from fastapi import APIRouter ,File,  UploadFile, Form
from src.service.ai_service import Agent
from src.utils.logs_setting import log_setting
from src.provider.ElasticsearchService import ElasticsearchService
from src.models.faceVerifyController.faceVerifyControllerModel import imgPairsModel


logger = log_setting(file_name="AI_Service", logs_tag = "AI_Service")
compare_endpoint = APIRouter()

ai_agent = Agent()
es = ElasticsearchService()

@compare_endpoint.post('/1-1')
async def face_verify(img1: UploadFile = File(), img2: UploadFile = File()) -> dict:

    img_obj = imgPairsModel(
        img1 = img1.file.read(),
        img1_name = img1.filename,
        img2 = img2.file.read(),
        img2_name = img1.filename
        )

    try:
        similarity_score = ai_agent.face_verify(img_obj)
        return {"response" : "200", "msg" : similarity_score}
    except Exception as e:
        return {"response": "500","msg" : str(e)}
