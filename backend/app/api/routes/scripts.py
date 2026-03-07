from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.models import Script, ScriptPublic
from app.core.db import get_db

router = APIRouter(prefix="/scripts", tags=["scripts"])


@router.get("/", response_model=list[ScriptPublic])
def get_scripts(session: Session = Depends(get_db)):
    return session.exec(select(Script)).all()
