from fastapi import APIRouter, Depends, Query
from sqlmodel import select, Session
from sqlalchemy.orm import selectinload
from sqlalchemy import func

from app.core.db import get_db
from app.models import Book, BookPublic, Manuscript, MSAdditionalInfo, Subject

router = APIRouter()


@router.get("/", response_model=list[BookPublic])
def get_books(
    subject: str | None = Query(default=None), session: Session = Depends(get_db)
):
    statement = select(Book).options(
        selectinload(Book.manuscripts).selectinload(Manuscript.subject),
        selectinload(Book.manuscripts).selectinload(Manuscript.additional_info),
    )

    if subject:
        statement = (
            statement.join(Book.manuscripts)
            .join(Manuscript.subject)
            .where(func.lower(Subject.name) == subject.lower())
            .distinct()  # ✅ prevents duplicate books
        )

    books = session.exec(statement).all()

    response = []

    for book in books:
        book_dict = book.model_dump()

        if book.manuscripts:
            first_manuscript = book.manuscripts[0]

            book_dict["original_title"] = first_manuscript.name or "—"
            book_dict["manuscript_id"] = first_manuscript.id

            if first_manuscript.additional_info:
                first_info = first_manuscript.additional_info[0]
                book_dict["author_name"] = first_info.author_name or "—"
            else:
                book_dict["author_name"] = "—"

        else:
            book_dict["original_title"] = "—"
            book_dict["author_name"] = "—"
            book_dict["manuscript_id"] = None

        response.append(book_dict)

    return response
