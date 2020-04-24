from sqlalchemy.orm import Session
from .base_class import Base


def add_and_commit(db: Session, model: Base):
    db.add(model)
    db.commit()
    db.refresh(model)
