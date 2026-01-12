from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_root_admin
from app.models.root_admin import RootAdmin
from app.schemas.queue import QueueCreate
from app.core.security import verify_password, create_jwt
from pydantic import BaseModel

router = APIRouter(tags=["root"])

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
def root_login(login_data: LoginRequest, db: Session = Depends(get_db)):
    admin = db.query(RootAdmin).filter_by(username=login_data.username).first()

    if not admin or not verify_password(login_data.password, admin.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_jwt({
        "role": "root",
        "root_id": str(admin.id)
    })

    return {"access_token": token}

@router.post("/queues")
def create_queue(
    data: QueueCreate,
    db: Session = Depends(get_db),
    root=Depends(get_root_admin)
):
    queue = Queue(
        id=uuid.uuid4(),
        name=data.name,
        type=data.type,
        address=data.address,
        image_name=data.image_name
    )

    db.add(queue)
    db.commit()
    db.refresh(queue)

    return {
        "id": queue.id
    }

@router.get("/queues")
def list_queues(
    db: Session = Depends(get_db)
):
    return db.query(Queue).all()
