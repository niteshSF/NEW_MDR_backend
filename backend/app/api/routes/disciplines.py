from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from app.models import Discipline, Branch, Subject, DisciplinePublic
from app.core.db import get_db

router = APIRouter(tags=["disciplines"])

# GET ALL DISCIPLINES OF A BRANCH (Nested)


@router.get(
    "/branches/{branch_id}/disciplines/",
    response_model=list[DisciplinePublic],
)
def get_disciplines_by_branch(
    branch_id: int,
    session: Session = Depends(get_db),
):
    branch = session.get(Branch, branch_id)
    if not branch:
        raise HTTPException(status_code=404, detail="Branch not found")

    statement = (
        select(Discipline)
        .where(Discipline.branch_id == branch_id)
        .options(selectinload(Discipline.subjects))
    )

    disciplines = session.exec(statement).all()
    return disciplines


# GET SINGLE DISCIPLINE (Nested)


@router.get(
    "/branches/{branch_id}/disciplines/{discipline_id}",
    response_model=DisciplinePublic,
)
def get_discipline_under_branch(
    branch_id: int,
    discipline_id: int,
    session: Session = Depends(get_db),
):
    statement = (
        select(Discipline)
        .where(
            Discipline.id == discipline_id,
            Discipline.branch_id == branch_id,
        )
        .options(selectinload(Discipline.subjects))
    )

    discipline = session.exec(statement).first()

    if not discipline:
        raise HTTPException(
            status_code=404,
            detail="Discipline not found under this branch",
        )

    return discipline
