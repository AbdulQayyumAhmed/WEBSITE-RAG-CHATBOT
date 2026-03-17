from fastapi import FastAPI
from app.database import Base, engine
from app.routes import user_routes, website_routes, chat_routes

app = FastAPI(title="Website RAG Chatbot API")

# Create all tables if not exists
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(user_routes.router)
app.include_router(website_routes.router)
app.include_router(chat_routes.router)

@app.get("/")
def root():
    return {"message": "RAG Chatbot API Running"}