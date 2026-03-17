from fastapi import Depends, HTTPException, Header
from app.database import SessionLocal
from app.models import User
from app.core.security import decode_access_token

def get_current_user(Authorization: str = Header(...)):
    """
    Expects: Authorization: Bearer <token>
    """
    if not Authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid auth header")
    token = Authorization.split(" ")[1]
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    db = SessionLocal()
    user = db.query(User).filter(User.id == payload.get("user_id")).first()
    db.close()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user