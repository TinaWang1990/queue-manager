from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from uuid import UUID

from app.dependencies import get_db, get_admin
from app.models.queue_entry import QueueEntry
from app.models.note import Note
from app.models.queue import Queue
from app.models.user import User
from app.schemas import admin as schemas

router = APIRouter(tags=["admin"])

@router.patch(
    "/patient/{entry_id}/status",
    response_model=schemas.StatusUpdateResponse
)
def update_patient_status(
    entry_id: UUID,
    status_update: schemas.StatusUpdateRequest,
    db: Session = Depends(get_db),
    admin=Depends(get_admin)
):
    """
    Update patient status
    - Valid statuses: waiting, processing, done, cancelled
    - Automatically sets timestamps for processing/done
    """
    entry = db.query(QueueEntry).filter(QueueEntry.id == entry_id).first()
    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Queue entry not found"
        )
    
    # Update status
    entry.status = status_update.status.value
    entry.updated_by = admin.username
    
    # Set timestamps based on status
    now = datetime.utcnow()
    if status_update.status == schemas.PatientStatus.PROCESSING:
        entry.processing_at = now
    elif status_update.status == schemas.PatientStatus.DONE:
        entry.done_at = now
    elif status_update.status == schemas.PatientStatus.CANCELLED:
        # Clear processing timestamp if cancelled
        entry.processing_at = None
    
    db.commit()
    db.refresh(entry)
    
    return schemas.StatusUpdateResponse(
        entry_id=entry.id,
        new_status=entry.status,
        updated_by=entry.updated_by,
        updated_at=now,
        processing_at=entry.processing_at,
        done_at=entry.done_at
    )

@router.post(
    "/queues/{queue_id}/notes",
    response_model=schemas.NoteCreateResponse,
    status_code=status.HTTP_201_CREATED
)
def publish_note(
    queue_id: UUID,
    note_data: schemas.NoteCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_admin)
):
    """
    Publish a note to a queue
    - Notes are visible to all patients in the queue
    """
    # Verify queue exists
    queue = db.query(Queue).filter(Queue.id == queue_id).first()
    if not queue:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Queue not found"
        )
    
    # Create note
    note = Note(
        queue_id=queue_id,
        message=note_data.message
    )
    
    db.add(note)
    db.commit()
    db.refresh(note)
    
    return schemas.NoteCreateResponse(
        note=schemas.NoteOut.from_orm(note)
    )

@router.get("/queues/{queue_id}/stats", response_model=schemas.QueueStats)
def get_queue_stats(
    queue_id: UUID,
    db: Session = Depends(get_db),
    admin=Depends(get_admin)
):
    """Get statistics for a specific queue"""
    # Verify admin has access to this queue
    if str(admin.queue_id) != str(queue_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized for this queue"
        )
    
    # Calculate statistics
    total_waiting = db.query(QueueEntry).filter(
        QueueEntry.queue_id == queue_id,
        QueueEntry.status == "waiting"
    ).count()
    
    total_processing = db.query(QueueEntry).filter(
        QueueEntry.queue_id == queue_id,
        QueueEntry.status == "processing"
    ).count()
    
    # Count done entries from today
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    total_done_today = db.query(QueueEntry).filter(
        QueueEntry.queue_id == queue_id,
        QueueEntry.status == "done",
        QueueEntry.done_at >= today_start
    ).count()
    
    # Calculate average wait time for done entries today
    done_entries = db.query(QueueEntry).filter(
        QueueEntry.queue_id == queue_id,
        QueueEntry.status == "done",
        QueueEntry.done_at >= today_start,
        QueueEntry.registered_at.isnot(None),
        QueueEntry.processing_at.isnot(None)
    ).all()
    
    avg_wait_time = 0.0
    if done_entries:
        total_wait = sum([
            (entry.processing_at - entry.registered_at).total_seconds()
            for entry in done_entries
        ])
        avg_wait_time = total_wait / len(done_entries) / 60  # Convert to minutes
    
    return schemas.QueueStats(
        total_waiting=total_waiting,
        total_processing=total_processing,
        total_done_today=total_done_today,
        average_wait_time_minutes=round(avg_wait_time, 1)
    )

@router.post("/bulk/status", response_model=schemas.BulkStatusResponse)
def bulk_update_status(
    bulk_update: schemas.BulkStatusUpdate,
    db: Session = Depends(get_db),
    admin=Depends(get_admin)
):
    """Update status for multiple patients at once"""
    updated_count = 0
    failed_entries = []
    now = datetime.utcnow()
    
    for entry_id in bulk_update.entry_ids:
        entry = db.query(QueueEntry).filter(QueueEntry.id == entry_id).first()
        if not entry:
            failed_entries.append(entry_id)
            continue
            
        # Update entry
        entry.status = bulk_update.status.value
        entry.updated_by = admin.username
        
        if bulk_update.status == schemas.PatientStatus.PROCESSING:
            entry.processing_at = now
        elif bulk_update.status == schemas.PatientStatus.DONE:
            entry.done_at = now
            
        updated_count += 1
    
    if updated_count > 0:
        db.commit()
    
    return schemas.BulkStatusResponse(
        updated_count=updated_count,
        failed_entries=failed_entries,
        ok=True
    )