from src.controllers.testController import train_endpoint
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(train_endpoint, prefix='/test',tags=["test"])