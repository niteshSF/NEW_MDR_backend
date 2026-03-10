from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from sqlalchemy import func
from typing import Dict, Optional

from app.core.db import get_db
from app.models import (
    Book,
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

router = APIRouter(prefix="/manuscripts", tags=["manuscripts"])


# ------------------------------
# GET ALL MANUSCRIPTS (FULL NESTED)
# ------------------------------
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
        statement = statement.join(Manuscript.subject).where(
            func.lower(Subject.name) == subject.lower()
        )

    if published is not None:
        statement = statement.where(Manuscript.published == published)

    manuscripts = session.exec(statement).all()
    return manuscripts


# ------------------------------
# GET COUNTS PER SUBJECT / TOPIC
# ------------------------------
@router.get("/counts")
def get_counts(subject: str, session: Session = Depends(get_db)) -> Dict:
    # Total manuscripts
    total_manuscripts = session.exec(
        select(func.count())
        .select_from(Manuscript)
        .join(Manuscript.subject)
        .where(func.lower(Subject.name) == subject.lower())
    ).one()

    # Total unique books linked to manuscripts of this subject
    total_books = session.exec(
        select(func.count(func.distinct(Book.id)))
        .select_from(Book)
        .join(Manuscript, Book.id == Manuscript.book_id)
        .join(Manuscript.subject)
        .where(func.lower(Subject.name) == subject.lower())
    ).one()

    # Total articles
    total_articles = session.exec(
        select(func.count())
        .select_from(Manuscript)
        .join(Manuscript.subject)
        .join(Manuscript.type)
        .where(
            func.lower(Subject.name) == subject.lower(),
            func.lower(Type.name) == "article",
        )
    ).one()

    return {
        "Documents": total_manuscripts + total_books,
        "Manuscripts": total_manuscripts,
        "Books": total_books,
        "Articles": total_articles,
    }


# ------------------------------
# GET DASHBOARD COUNTS PER BRANCH
# ------------------------------
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
        select(func.count(func.distinct(Book.id)))
        .select_from(Book)
        .join(Manuscript, Book.id == Manuscript.book_id)
        .join(Manuscript.subject)
        .join(Subject.discipline)
        .join(Discipline.branch)
        .where(func.lower(Branch.short_name) == branch.lower())
    ).one()

    total_articles = session.exec(
        select(func.count())
        .select_from(Manuscript)
        .join(Manuscript.subject)
        .join(Subject.discipline)
        .join(Discipline.branch)
        .join(Manuscript.type)
        .where(
            func.lower(Branch.short_name) == branch.lower(),
            func.lower(Type.name) == "article",
        )
    ).one()

    total_documents = total_manuscripts + total_books

    return {
        "Documents": total_documents,
        "Manuscripts": total_manuscripts,
        "Books": total_books,
        "Articles": total_articles,
    }


# ------------------------------
# GET COUNTS PER DISCIPLINE
# ------------------------------
@router.get("/discipline-counts")
def get_discipline_counts(discipline: str, session: Session = Depends(get_db)) -> Dict:
    total_manuscripts = session.exec(
        select(func.count())
        .select_from(Manuscript)
        .join(Manuscript.subject)
        .join(Subject.discipline)
        .where(func.lower(Discipline.name) == discipline.lower())
    ).one()

    total_books = session.exec(
        select(func.count(func.distinct(Book.id)))
        .select_from(Book)
        .join(Manuscript, Book.id == Manuscript.book_id)
        .join(Manuscript.subject)
        .join(Subject.discipline)
        .where(func.lower(Discipline.name) == discipline.lower())
    ).one()

    total_articles = session.exec(
        select(func.count())
        .select_from(Manuscript)
        .join(Manuscript.subject)
        .join(Subject.discipline)
        .join(Manuscript.type)
        .where(
            func.lower(Discipline.name) == discipline.lower(),
            func.lower(Type.name) == "article",
        )
    ).one()

    total_documents = total_manuscripts + total_books

    return {
        "Discipline": discipline,
        "Documents": total_documents,
        "Manuscripts": total_manuscripts,
        "Books": total_books,
        "Articles": total_articles,
    }


# ------------------------------
# GET MANUSCRIPT BY ID
# ------------------------------
@router.get("/{id}", response_model=ManuscriptPublic)
def get_manuscript_by_id(id: int, session: Session = Depends(get_db)):
    statement = (
        select(Manuscript)
        .where(Manuscript.id == id)
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
