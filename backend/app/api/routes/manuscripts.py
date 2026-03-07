from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from app.models import (
    Manuscript,
    Language,
    Script,
    Category,
    Type,
    Tag,
    MSAdditionalInfo,
    ManuscriptPublic,
    Subject,
    Discipline,
    Branch,
)
from app.core.db import get_db
from sqlalchemy import func
from typing import Dict

router = APIRouter(prefix="/manuscripts", tags=["manuscripts"])


# GET ALL MANUSCRIPTS (FULL NESTED)

from typing import Optional
from fastapi import Query


from typing import Optional
from fastapi import Query


@router.get("/", response_model=list[ManuscriptPublic])
def get_manuscripts(
    subject: Optional[str] = Query(default=None),
    published: Optional[bool] = Query(default=None),
    session: Session = Depends(get_db),
):

    statement = select(Manuscript).options(
        selectinload(Manuscript.language),
        selectinload(Manuscript.script),
        selectinload(Manuscript.category),
        selectinload(Manuscript.type),
        selectinload(Manuscript.tags),
        selectinload(Manuscript.additional_info),
        selectinload(Manuscript.book),
        selectinload(Manuscript.subject)
        .selectinload(Subject.discipline)
        .selectinload(Discipline.branch),
    )

    if subject:
        statement = statement.join(Subject).where(
            func.lower(Subject.name) == subject.lower()
        )

    if published is not None:
        statement = statement.where(Manuscript.published == published)

    manuscripts = session.exec(statement).all()

    return manuscripts


@router.get("/counts")
def get_counts(subject: str, session: Session = Depends(get_db)) -> Dict:

    total_manuscripts = session.exec(
        select(func.count())
        .select_from(Manuscript)
        .join(Subject)
        .where(func.lower(Subject.name) == subject.lower())
    ).one()

    total_books = session.exec(
        select(func.count())
        .select_from(Manuscript)
        .join(Subject)
        .where(
            func.lower(Subject.name) == subject.lower(),
            Manuscript.published == True,
        )
    ).one()

    return {
        "Manuscripts": total_manuscripts,
        "Books": total_books,
        "Articles": 0,
    }


@router.get("/dashboard-counts-branch")
def get_dashboard_counts_by_branch(
    branch: str, session: Session = Depends(get_db)
) -> Dict:

    total_manuscripts = session.exec(
        select(func.count())
        .select_from(Manuscript)
        .join(Manuscript.subject)
        .join(Subject.discipline)
        .join(Discipline.branch)
        .where(func.lower(Branch.short_name) == branch.lower())
    ).one()

    total_books = session.exec(
        select(func.count())
        .select_from(Manuscript)
        .join(Manuscript.subject)
        .join(Subject.discipline)
        .join(Discipline.branch)
        .where(
            func.lower(Branch.short_name) == branch.lower(),
            Manuscript.published == True,
        )
    ).one()

    total_articles = 0

    total_documents = total_manuscripts + total_books

    return {
        "Documents": total_documents,
        "Manuscripts": total_manuscripts,
        "Books": total_books,
        "Articles": total_articles,
    }


@router.get("/discipline-counts")
def get_discipline_counts(
    discipline: str,
    session: Session = Depends(get_db),
) -> Dict:

    # Total manuscripts inside discipline (all subjects)
    total_manuscripts = session.exec(
        select(func.count())
        .select_from(Manuscript)
        .join(Subject)
        .join(Discipline)
        .where(func.lower(Discipline.name) == discipline.lower())
    ).one()

    # Total books (published=True)
    total_books = session.exec(
        select(func.count())
        .select_from(Manuscript)
        .join(Subject)
        .join(Discipline)
        .where(
            func.lower(Discipline.name) == discipline.lower(),
            Manuscript.published == True,
        )
    ).one()

    total_articles = 0

    total_documents = total_manuscripts + total_books

    return {
        "Discipline": discipline,
        "Documents": total_documents,
        "Manuscripts": total_manuscripts,
        "Books": total_books,
        "Articles": total_articles,
    }


@router.get("/{accession_number}", response_model=ManuscriptPublic)
def get_manuscript_by_code(accession_number: str, session: Session = Depends(get_db)):
    statement = (
        select(Manuscript)
        .where(Manuscript.accession_number == accession_number)
        .options(
            selectinload(Manuscript.language),
            selectinload(Manuscript.script),
            selectinload(Manuscript.category),
            selectinload(Manuscript.type),
            selectinload(Manuscript.tags),
            selectinload(Manuscript.additional_info),
            selectinload(Manuscript.book),
            selectinload(Manuscript.subject)
            .selectinload(Subject.discipline)
            .selectinload(Discipline.branch),
        )
    )

    manuscript = session.exec(statement).first()

    if not manuscript:
        raise HTTPException(status_code=404, detail="Manuscript not found")

    return manuscript
