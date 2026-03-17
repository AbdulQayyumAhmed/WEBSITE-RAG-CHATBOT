from datetime import datetime, timedelta
from typing import Optional
import jwt
from app.core.config import GEMINI_API_KEY  # We'll add JWT_SECRET in .env
from passlib.context import CryptContext

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

JWT_SECRET = "myjwtsecret"  # For testing, move to .env for production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# core/security.py

# Hashing temporarily removed
def get_password_hash(password: str) -> str:
    return password  # plain password

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return plain_password == hashed_password  # simple check

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None