import os
import uuid
import fitz
import re
from semantic_text_splitter import TextSplitter
from tokenizers import Tokenizer
from dotenv import load_dotenv

load_dotenv()
MODEL_ID = os.getenv("MODEL_ID")
tokenizer = Tokenizer.from_pretrained(MODEL_ID)
textSplitter = TextSplitter.from_huggingface_tokenizer(tokenizer)

def extract_text_from_pdf(file_contents):
    # file_contents is a bytes object
    # generate a temporary file and write the contents of file_contents to it
    # generate a random filename
    filename = f"temp/{uuid.uuid4()}.pdf"
    with open(filename, "wb") as f:
        f.write(file_contents.read())

    doc = fitz.open(filename)
    text = " ".join([page.get_text() for page in doc])

    # delete the temporary file
    os.remove(filename)

    return text

def preprocess_text(text):
    # Remove unnecessary spaces (more than one)
    text = re.sub(r'\s+', ' ', text)
    # Remove unnecessary \n (more than one)
    text = re.sub(r'\n+', '\n', text)
    # Define a list of unnecessary symbols
    unnecessary_symbols = ['.', ',', ';', ':', '!', '?', '*', '$', '%', '@', '#', '&', '•']
    # Replace multiple instances of unnecessary symbols with just one instance
    for symbol in unnecessary_symbols:
        text = re.sub(r'({})+'.format(re.escape(symbol)), symbol, text)

    return text

def split_text(text, chunk_size):
    chunks = textSplitter.chunks(text, int(chunk_size))
    return chunks