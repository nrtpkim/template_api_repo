import uvicorn
from fastapi import FastAPI
from src.controllers import api_router


app = FastAPI()
app.include_router(api_router)



if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=7001, reload=True) # worker=2
