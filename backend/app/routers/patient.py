import uuid
from datetime import datetime
from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.schemas.patient import JoinQueue
from app.models.user import User
from app.models.queue_entry import QueueEntry
from app.services.wait_time import estimated_wait

router = APIRouter(tags=["patient"])

@router.post("/join/{queue_id}")
def join_queue(queue_id: uuid.UUID, data: JoinQueue, db: Session = Depends(get_db)):
    user = User(username=data.username, phone=data.phone)
    db.add(user)
    db.flush()

    entry = QueueEntry(
        queue_id=queue_id,
        user_id=user.id,
        status="registered",
        updated_by="patient",
        registered_at=datetime.utcnow()
    )

    db.add(entry)
    db.commit()

    return {
        "patient_id": user.id,
        "session_token": entry.id
    }

@router.get("/status")
def get_status(
    session_token: str = Header(...),
    db: Session = Depends(get_db)
):
    entry = db.query(QueueEntry).filter_by(id=session_token).first()

    position = db.query(QueueEntry).filter(
        QueueEntry.queue_id == entry.queue_id,
        QueueEntry.status == "registered",
        QueueEntry.registered_at < entry.registered_at
    ).count()

    wait = estimated_wait(db, entry.queue_id, position)

    return {
        "status": entry.status,
        "updated_by": entry.updated_by,
        "position": position,
        "estimated_wait_minutes": wait
    }