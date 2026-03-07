from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.models import Type, TypePublic
from app.core.db import get_db

router = APIRouter(prefix="/types", tags=["types"])


@router.get("/", response_model=list[TypePublic])
def get_types(session: Session = Depends(get_db)):
    return session.exec(select(Type)).all()
