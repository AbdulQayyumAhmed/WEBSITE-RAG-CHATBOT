from app.embeddings import collection, create_embedding
import google.generativeai as genai
from app.core.config import GEMINI_API_KEY
import re

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")


def retrieve_chunks(question, top_k=3):
    """Retrieve top relevant chunks from vector DB"""
    embedding = create_embedding(question)
    results = collection.query(
        query_embeddings=[embedding],
        n_results=top_k
    )
    return results["documents"][0] if results["documents"] else []


def clean_text(text):
    """Clean text: remove extra spaces, newlines, HTML tags"""
    text = re.sub(r'\s+', ' ', text)  # multiple spaces/newlines → single space
    text = re.sub(r'<.*?>', '', text)  # remove HTML tags if any
    return text.strip()


def rag_answer(question):
    """Generate response using RAG pipeline and clean output"""
    chunks = retrieve_chunks(question)
    context = "\n".join(chunks)
    
    prompt = f"""
Context:
{context}

Question:
{question}

Answer using only the context. Keep it concise and clear.
"""

    response = model.generate_content(prompt)
    text = response.text if hasattr(response, 'text') else str(response)

    return clean_text(text)