import chromadb
from sentence_transformers import SentenceTransformer

# Chroma vector DB
client = chromadb.Client()
collection = client.get_or_create_collection(
    name="website_embeddings"
)

# Sentence transformer model
model = SentenceTransformer("all-MiniLM-L6-v2")

def create_embedding(text):
    """Convert text to embedding vector"""
    return model.encode(text).tolist()

def store_chunk(chunk_text, website_id):
    """Store chunk + embedding in Chroma DB"""
    embedding = create_embedding(chunk_text)

    collection.add(
        documents=[chunk_text],
        embeddings=[embedding],
        metadatas=[{"website_id": website_id}],
        ids=[f"{website_id}_{hash(chunk_text)}"]
    )