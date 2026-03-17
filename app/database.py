from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import DATABASE_URL

# PostgreSQL ke liye engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True  # server disconnect handle karne ke liye
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for models
Base = declarative_base()

# Dependency for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Optional: startup me tables create karna
def init_db():
    from app.models import User, Website, ChatHistory
    Base.metadata.create_all(bind=engine)