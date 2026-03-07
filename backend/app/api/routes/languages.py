from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.models import Language, LanguagePublic
from app.core.db import get_db

router = APIRouter(prefix="/languages", tags=["languages"])


@router.get("/", response_model=list[LanguagePublic])
def get_languages(session: Session = Depends(get_db)):
    return session.exec(select(Language)).all()
