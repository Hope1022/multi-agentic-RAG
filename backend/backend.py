from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.schema import User_question, AI_Response
from main import run


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/chat")

def user_question(body:User_question):#
    response = run(body.question)
    
    return {"response":response}
    