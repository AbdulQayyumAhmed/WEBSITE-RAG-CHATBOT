from fastapi import APIRouter
from app.rag_pipeline import rag_answer
import google.generativeai as genai
from app.core.config import GEMINI_API_KEY
import re

router = APIRouter()
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")


def clean_text(text):
    """Clean LLM output"""
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'<.*?>', '', text)
    return text.strip()


@router.post("/chat")
def chat(message: str, use_website: bool = False):
    if use_website:
        response = rag_answer(message)
        mode = "website"
    else:
        raw_response = model.generate_content(message)
        response = clean_text(raw_response.text if hasattr(raw_response, "text") else str(raw_response))
        mode = "general"

    return {"mode": mode, "response": response}