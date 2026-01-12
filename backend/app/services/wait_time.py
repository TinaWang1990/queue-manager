from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.queue_entry import QueueEntry

def calculate_average_wait(db: Session, queue_id):
    result = db.query(
        func.avg(QueueEntry.done_at - QueueEntry.registered_at)
    ).filter(
        QueueEntry.queue_id == queue_id,
        QueueEntry.done_at.isnot(None)
    ).scalar()

    if not result:
        return 5  # default minutes

    return int(result.total_seconds() / 60)

def estimated_wait(db: Session, queue_id, position: int):
    avg = db.query(
        func.avg(QueueEntry.done_at - QueueEntry.registered_at)
    ).filter(
        QueueEntry.queue_id == queue_id,
        QueueEntry.done_at.isnot(None)
    ).scalar()

    minutes = 5 if not avg else int(avg.total_seconds() / 60)
    return position * minutes