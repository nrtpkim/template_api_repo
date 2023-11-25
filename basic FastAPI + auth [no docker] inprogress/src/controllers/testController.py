from fastapi import APIRouter
from src.services.test_service import Agent


train_endpoint = APIRouter()

@train_endpoint.post('/1-1')
async def hello(text: str):

    try:
        res = Agent().run(text)
        return {"response" : "200", "msg" : res}
    except Exception as e:
        return {"response": "500","msg" : str(e)}

