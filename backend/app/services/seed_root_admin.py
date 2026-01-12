from sqlalchemy.orm import Session
from app.models.root_admin import RootAdmin
from app.core.security import hash_password

DEFAULT_ROOT_USERNAME = "shihuiwang1990@gmail.com"
DEFAULT_ROOT_PASSWORD = "root"

def seed_root_admin(db: Session):
    exists = db.query(RootAdmin).filter(
        RootAdmin.username == DEFAULT_ROOT_USERNAME
    ).first()

    if exists:
        return

    root = RootAdmin(
        username=DEFAULT_ROOT_USERNAME,
        password_hash=hash_password(DEFAULT_ROOT_PASSWORD)
    )

    db.add(root)
    db.commit()
    print("✅ Root admin created")
