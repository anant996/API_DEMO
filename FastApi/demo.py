from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

app=FastAPI()

demo_db = {
    "anant": {
        "username": "anant",
        "password": "123@Pune",
        "email": "ac@gmail.com",
    },
    "raj": {
        "username": "raj",
        "password": "123@Kharadi",
        "email": "raj@gmail.com",
    }
}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

prompt_value="You're an esteemed college professor tasked with crafting {type} questions based on the {content} provided."

class Prompt(BaseModel):
    type: str
    content: str

@app.post("/set_prompt/")
async def set_prompt(prompt: Prompt, token: Annotated[str, Depends(oauth2_scheme)]):
    global prompt_value
    prompt_value = f"You're an esteemed college professor tasked with crafting {prompt.type} questions based on the {prompt.content} provided."
    return {"message": "Prompt value updated successfully"}

@app.get("/get_prompt/")
async def get_prompt(token: Annotated[str, Depends(oauth2_scheme)]):
    global prompt_value
    return {"prompt_value": prompt_value}

@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"access_token": form_data.username, "token_type": "bearer"}

def authenticate_user(username: str, password: str):
    user = demo_db.get(username)
    if user and user["password"] == password:
        return user

@app.get("/valid_user/")
async def valid_user(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"message": "This is a valid user", "token": token}
