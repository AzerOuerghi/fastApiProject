from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from llm import boto3_invoke_model

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


class PromptRequest(BaseModel):
    prompt: str


@app.post("/hello")
async def say_hello(request: PromptRequest):
    res = boto3_invoke_model(request.prompt)
    return {"response": res}
