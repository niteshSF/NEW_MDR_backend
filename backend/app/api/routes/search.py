from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from app.core.db import get_db
from app.models import (
    Manuscript,
    MSAdditionalInfo,
    Book,
    Language,
    Script,
    Category,
    Type,
    Subject,
    Discipline,
    Branch,
)

router = APIRouter(tags=["search"])


# -------------------------------
# GET SEARCH RESULTS
# -------------------------------
@router.get("/search")
def search_documents(
    document_id: str = None,
    document_name: str = None,
    subject: int = None,
    language: int = None,
    script: int = None,
    doc_type: int = None,
    category: int = None,
    author: str = None,
    source_name: str = None,
    db: Session = Depends(get_db),
):
    query = (
        db.query(Manuscript)
        .join(
            MSAdditionalInfo,
            Manuscript.id == MSAdditionalInfo.manuscript_id,
            isouter=True,
        )
        .join(Book, Manuscript.book_id == Book.id, isouter=True)
        .join(Subject, Manuscript.subject_id == Subject.id, isouter=True)
        .join(Discipline, Subject.discipline_id == Discipline.id, isouter=True)
        .join(Branch, Discipline.branch_id == Branch.id, isouter=True)
        .join(Type, Manuscript.type_id == Type.id, isouter=True)
    )

    filters = []

    if document_id:
        filters.append(Manuscript.accession_number.like(f"%{document_id}%"))
    if document_name:
        filters.append(func.lower(Manuscript.name).like(f"%{document_name.lower()}%"))
    if subject:
        filters.append(Manuscript.subject_id == subject)
    if language:
        filters.append(Manuscript.language_id == language)
    if script:
        filters.append(Manuscript.script_id == script)
    if doc_type:
        filters.append(Manuscript.type_id == doc_type)
    if category:
        filters.append(Manuscript.category_id == category)
    if author:
        filters.append(MSAdditionalInfo.author_name.like(f"%{author}%"))
    if source_name:
        filters.append(Book.published_title.like(f"%{source_name}%"))

    if filters:
        query = query.filter(and_(*filters))

    results = query.all()

    # Prepare response
    response = []
    for m in results:
        branch = (
            m.subject.discipline.branch.name
            if m.subject and m.subject.discipline and m.subject.discipline.branch
            else None
        )
        discipline = (
            m.subject.discipline.name if m.subject and m.subject.discipline else None
        )

        response.append(
            {
                "id": m.id,
                "name": m.name,
                "document_type": "Book" if m.book_id else "Manuscript",
                "subject": (
                    {
                        "id": m.subject.id if m.subject else None,
                        "name": m.subject.name if m.subject else None,
                        "discipline": (
                            {
                                "id": (
                                    m.subject.discipline.id
                                    if m.subject and m.subject.discipline
                                    else None
                                ),
                                "name": discipline,
                                "branch": (
                                    {
                                        "id": (
                                            m.subject.discipline.branch.id
                                            if m.subject
                                            and m.subject.discipline
                                            and m.subject.discipline.branch
                                            else None
                                        ),
                                        "name": branch,
                                    }
                                    if branch
                                    else None
                                ),
                            }
                            if discipline
                            else None
                        ),
                    }
                    if m.subject
                    else None
                ),
            }
        )

    return response


# -------------------------------
# GET OPTIONS FOR DROPDOWNS
# -------------------------------
@router.get("/search/options")
def get_options(db: Session = Depends(get_db)):
    return {
        "languages": db.query(Language).all(),
        "scripts": db.query(Script).all(),
        "categories": db.query(Category).all(),
        "types": db.query(Type).all(),
        "subjects": db.query(Subject).all(),
    }
