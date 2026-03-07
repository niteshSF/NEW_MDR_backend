from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.models import Subject, Discipline, Branch, SubjectPublic
from app.core.db import get_db

router = APIRouter(tags=["subjects"])


# Get all subjects under a discipline of a branch
@router.get(
    "/branches/{branch_id}/disciplines/{discipline_id}/subjects/",
    response_model=list[SubjectPublic],
)
def get_subjects_by_discipline(
    branch_id: int,
    discipline_id: int,
    session: Session = Depends(get_db),
):
    # Check branch exists
    branch = session.get(Branch, branch_id)
    if not branch:
        raise HTTPException(status_code=404, detail="Branch not found")

    # Check discipline exists
    discipline = session.get(Discipline, discipline_id)
    if not discipline:
        raise HTTPException(status_code=404, detail="Discipline not found")

    # Check discipline belongs to branch
    if discipline.branch_id != branch_id:
        raise HTTPException(
            status_code=400,
            detail="Discipline does not belong to this branch",
        )

    statement = select(Subject).where(Subject.discipline_id == discipline_id)
    subjects = session.exec(statement).all()
    return subjects


# Get specific subject under discipline + branch
@router.get(
    "/branches/{branch_id}/disciplines/{discipline_id}/subjects/{subject_id}",
    response_model=SubjectPublic,
)
def get_subject_under_discipline(
    branch_id: int,
    discipline_id: int,
    subject_id: int,
    session: Session = Depends(get_db),
):
    branch = session.get(Branch, branch_id)
    if not branch:
        raise HTTPException(status_code=404, detail="Branch not found")

    discipline = session.get(Discipline, discipline_id)
    if not discipline:
        raise HTTPException(status_code=404, detail="Discipline not found")

    if discipline.branch_id != branch_id:
        raise HTTPException(
            status_code=400,
            detail="Discipline does not belong to this branch",
        )

    subject = session.get(Subject, subject_id)
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")

    if subject.discipline_id != discipline_id:
        raise HTTPException(
            status_code=400,
            detail="Subject does not belong to this discipline",
        )

    return subject
