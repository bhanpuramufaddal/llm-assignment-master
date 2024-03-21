import os
import re

from app.utils import extract_text_from_pdf, preprocess_text, split_text
from app.qa_model import QaModel
from app.vector_db import VectorDB

MODEL_ID = os.getenv("MODEL_ID")

class RagEngine:
    def __init__(self):
        self.chunk_size = os.getenv("CHUNK_SIZE")
        self.qaModel = QaModel()

    def get_chunks_from_pdf(self, file_contents):
        text = extract_text_from_pdf(file_contents)
        text = preprocess_text(text)
        return split_text(text, self.chunk_size)

    def get_most_relevant_chunk(self, query, chunks):
        vector_db = VectorDB(chunks)
        return vector_db.topk(query, k = 1)[0]

    def answer_question(self, query, file_contents):
        chunks = self.get_chunks_from_pdf(file_contents)
        most_relevant_chunk = self.get_most_relevant_chunk(query, chunks)
        return self.qaModel.answer(query, most_relevant_chunk)



    