import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base

class QueueEntry(Base):
    __tablename__ = "queue_entries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    queue_id = Column(UUID(as_uuid=True), ForeignKey("queues.id"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    status = Column(String, nullable=False)
    updated_by = Column(String, nullable=False)

    registered_at = Column(DateTime)
    processing_at = Column(DateTime)
    done_at = Column(DateTime)
