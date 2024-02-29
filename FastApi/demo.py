from fastapi import FastAPI
from pydantic import BaseModel

app=FastAPI()

prompt_value="You're an esteemed college professor tasked with crafting {type} questions based on the {content} provided."

class Prompt(BaseModel):
    type: str
    content: str
    
@app.post("/set_prompt/")
async def set_prompt(prompt: Prompt):
    global prompt_value
    prompt_value = f"You're an esteemed college professor tasked with crafting {prompt.type} questions based on the {prompt.content} provided."
    return {"message": "Prompt value updated successfully"}


@app.get("/get_prompt/")
async def get_prompt():
    global prompt_value
    return {"prompt_value": prompt_value}

