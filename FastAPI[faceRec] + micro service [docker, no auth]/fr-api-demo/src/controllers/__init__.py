from src.controllers.faceVerifyController import compare_endpoint
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(compare_endpoint, prefix='/verify',tags=["FaceVerify"])


