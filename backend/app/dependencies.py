from fastapi import Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.core.security import decode_jwt

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_admin(authorization: str = Header(...)):
    token = authorization.replace("Bearer ", "")
    payload = decode_jwt(token)
    if not payload or payload.get("role") not in ("admin", "root"):
        raise HTTPException(status_code=401, detail="Unauthorized")
    return payload

def get_root_admin(authorization: str = Header(...)):
    token = authorization.replace("Bearer ", "")
    payload = decode_jwt(token)

    if not payload or payload.get("role") != "root":
        raise HTTPException(status_code=403, detail="Root admin only")

    return payload