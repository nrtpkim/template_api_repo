from src.controllers.serviceController import endpoint
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(endpoint,tags=["test"]) # prefix = '/test'