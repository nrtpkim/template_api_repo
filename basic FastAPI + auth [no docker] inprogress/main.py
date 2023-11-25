import uvicorn
from fastapi import FastAPI, Form, Depends, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import Annotated

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Simulated user database
fake_users_db = {
    "user": {
        "username": "user",
        "password": "passwordx",
        "disabled": False,
    }
}

class UserPass(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    token: str = Depends(oauth2_scheme)

def verify_password(input_password, hashed_password):
    return input_password == hashed_password

def get_user(db, username: str):
    print('get_user DB:',db)
    if username in db:
        user_dict = db[username]
        print(user_dict)
        return user_dict

def authenticate_user(username: str, password: str):
    user = get_user(fake_users_db, username)
    print('db: ',user)
    print('input: ', username, password)
    if not user:
        print(user)
        return False
    if not verify_password(password, user["password"]):
        print(password, user["password"])
        return False
    return user


@app.post("/hello")
async def hello(name:str):
    return name


@app.post("/token")
async def login_for_access_token(UserPass:UserPass):
    user = authenticate_user(UserPass.username, UserPass.password)
    print(user)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    # Implement OAuth2 logic to generate and return access token
    return {"access_token": UserPass.username, "token_type": "bearer"}



@app.get("/protected")
async def protected_route(token: str = Depends(oauth2_scheme)):
# async def protected_route(Token:Token):
    # Implement logic to validate the token and allow access to protected route
    if Token.token != "user":
        raise HTTPException(status_code=403, detail="Forbidden")
    return {"message": "Access granted"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=7001, reload=True)



### TODO:
# 3. code basic FastAPI + auth [no docker]

