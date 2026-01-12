from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.models.queue import Queue
from app.schemas.queue import QueueOut

router = APIRouter(tags=["queues"])

@router.get("", response_model=list[QueueOut])
def list_queues(db: Session = Depends(get_db)):
    return db.query(Queue).filter(Queue.active == True).all()
