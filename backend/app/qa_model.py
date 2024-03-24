from transformers import AutoTokenizer, AutoModelForCausalLM
import re
import os
import dotenv

dotenv.load_dotenv()
MODEL_NAME = os.getenv("MODEL_ID")
HF_TOKEN = os.getenv("HF_TOKEN")    
QA_PROMPT = """Answr the question using the following context:
**Question**: {}

**Context**:
{}

**Answer**:
"""

class QaModel:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, token = HF_TOKEN)
        self.llm = AutoModelForCausalLM.from_pretrained(MODEL_NAME, token = HF_TOKEN)

    def generate_answer(self, prompt):
        input_ids = self.tokenizer(prompt, return_tensors="pt").input_ids
        outputs = self.llm.generate(input_ids, max_new_tokens=500)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

    def answer(self, question, context):
        prompt = QA_PROMPT.format(question, context)
        answer = self.generate_answer(prompt)
        answer = answer.replace(prompt, "")
        return answer