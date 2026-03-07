from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from app.models import Branch, Discipline, BranchPublic
from app.core.db import get_db

router = APIRouter(prefix="/branches", tags=["branches"])


# GET ALL BRANCHES (Nested)

@router.get("/", response_model=list[BranchPublic])
def get_branches(session: Session = Depends(get_db)):
    statement = select(Branch).options(
        selectinload(Branch.disciplines).selectinload(Discipline.subjects)
    )

    branches = session.exec(statement).all()
    return branches


@router.get("/{branch_id}", response_model=BranchPublic)
def get_branch(branch_id: int, session: Session = Depends(get_db)):
    statement = (
        select(Branch)
        .where(Branch.id == branch_id)
        .options(selectinload(Branch.disciplines).selectinload(Discipline.subjects))
    )

    branch = session.exec(statement).first()

    if not branch:
        raise HTTPException(status_code=404, detail="Branch not found")

    return branch
