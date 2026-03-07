from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.models import Tag, TagPublic
from app.core.db import get_db

router = APIRouter(prefix="/tags", tags=["tags"])


@router.get("/", response_model=list[TagPublic])
def get_tags(session: Session = Depends(get_db)):
    return session.exec(select(Tag)).all()
