from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Website
from app.scraper import scrape_website
from app.embeddings import store_chunk

router = APIRouter()

@router.post("/add-website")
def add_website(url: str, db: Session = Depends(get_db)):
    text = scrape_website(url, max_pages=50)  # scrape max 50 pages

    website = Website(
        user_id=1,  # default user
        url=url,
        status="processed"
    )
    db.add(website)
    db.commit()
    db.refresh(website)

    # Split text into chunks
    chunk_size = 500
    overlap = 50
    chunks = []

    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap

    # Store chunks in vector DB
    for chunk in chunks:
        store_chunk(chunk, website.id)

    return {"message": "Website processed successfully", "chunks_stored": len(chunks)}