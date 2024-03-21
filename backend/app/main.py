from dotenv import load_dotenv
from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel # PyMuPDF
import json
import os

from app.utils import preprocess_text

from app.rag_engine import RagEngine

# Load environment variables from .env file (if any)
load_dotenv()
os.makedirs('temp', exist_ok=True)
ragEngine = RagEngine()

origins = ["*"]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/predict")
async def predict(query:str = Form(...), file: UploadFile = File(...)):
    print("Request received")
    # Access request headers, cookies, etc. using the request object
    # fake_answer = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut pretium risus tellus, sit amet dictum eros molestie nec. Maecenas sit amet arcu placerat, varius felis non, gravida leo. Sed nisi felis, volutpat id quam tincidunt, lobortis dapibus eros. Integer tempor erat sit amet quam ornare scelerisque. Nullam gravida, dolor et ultricies aliquet, eros felis pulvinar nulla, vel feugiat lectus magna ac erat. Nunc quis purus sagittis, tincidunt mi finibus, molestie nulla. Aenean egestas dapibus diam, tincidunt tristique nisl faucibus eget. Curabitur tincidunt tortor lacus, nec rutrum est vulputate a. Donec pretium eleifend dignissim."""
    # return {
    #     "result": fake_answer
    # }
    result = ragEngine.answer_question(query, file.file)
    result = preprocess_text(result)
    return {"result": result}
