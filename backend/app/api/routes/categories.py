from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.models import Category, CategoryPublic
from app.core.db import get_db

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("/", response_model=list[CategoryPublic])
def get_categories(session: Session = Depends(get_db)):
    return session.exec(select(Category)).all()
