from pydantic import EmailStr
from typing import Optional
from sqlmodel import Field, Relationship, SQLModel


# Shared properties
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=128)
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on update, all are optional
class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore
    password: str | None = Field(default=None, min_length=8, max_length=128)


class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=128)
    new_password: str = Field(min_length=8, max_length=128)


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: int


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


# Shared properties
class EntityBase(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_by: Optional[int] = Field(default=None, foreign_key="user.id")
    created_at: Optional[str] = Field(default=None)
    updated_by: Optional[int] = Field(default=None, foreign_key="user.id")
    updated_at: Optional[str] = Field(default=None)
    active: bool = True


# Database model, database table inferred from class name
class Language(EntityBase, table=True):
    short_name: str = Field(unique=True, index=True, max_length=10)
    name: str = Field(unique=True, index=True, max_length=255)
    manuscripts: list["Manuscript"] = Relationship(
        back_populates="language",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )


class Script(EntityBase, table=True):
    short_name: str = Field(unique=True, index=True, max_length=10)
    name: str = Field(unique=True, index=True, max_length=255)
    manuscripts: list["Manuscript"] = Relationship(
        back_populates="script",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )


class Category(EntityBase, table=True):
    short_name: str = Field(unique=True, index=True, max_length=10)
    name: str = Field(unique=True, index=True, max_length=255)
    manuscripts: list["Manuscript"] = Relationship(
        back_populates="category",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )


class Type(EntityBase, table=True):
    short_name: str = Field(unique=True, index=True, max_length=10)
    name: str = Field(unique=True, index=True, max_length=255)
    manuscripts: list["Manuscript"] = Relationship(
        back_populates="type", sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )


# 1. Linking Table (Many-to-Many)
class ManuscriptTagLink(SQLModel, table=True):
    manuscript_id: Optional[int] = Field(
        default=None, foreign_key="manuscript.id", primary_key=True
    )
    tag_id: Optional[int] = Field(default=None, foreign_key="tag.id", primary_key=True)


class Tag(EntityBase, table=True):
    short_name: str = Field(index=True, max_length=10)  # new
    name: str = Field(unique=True, index=True, max_length=255)

    # Relationship to Manuscript
    manuscripts: list["Manuscript"] = Relationship(
        back_populates="tags", link_model=ManuscriptTagLink
    )


class Branch(EntityBase, table=True):
    short_name: str = Field(unique=True, index=True, max_length=10)
    name: str = Field(unique=True, index=True, max_length=255)
    indic_name: str = Field(unique=True, index=True, max_length=255)
    disciplines: list["Discipline"] = Relationship(
        back_populates="branch",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )


class Discipline(EntityBase, table=True):
    short_name: str = Field(unique=True, index=True, max_length=10)
    name: str = Field(unique=True, index=True, max_length=255)
    indic_name: str = Field(unique=True, index=True, max_length=255)
    branch_id: Optional[int] = Field(default=None, foreign_key="branch.id")
    branch: Optional[Branch] = Relationship(back_populates="disciplines")
    subjects: list["Subject"] = Relationship(
        back_populates="discipline",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )


class Subject(EntityBase, table=True):
    short_name: str = Field(unique=True, index=True, max_length=10)
    name: str = Field(unique=True, index=True, max_length=255)
    indic_name: str = Field(unique=True, index=True, max_length=255)
    discipline_id: Optional[int] = Field(default=None, foreign_key="discipline.id")
    discipline: Optional[Discipline] = Relationship(back_populates="subjects")
    manuscripts: list["Manuscript"] = Relationship(
        back_populates="subject",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )


class Book(EntityBase, table=True):
    published_title: str | None = Field(default=None, max_length=255)

    translator_name: str | None = Field(default=None, max_length=255)
    publisher_name: str | None = Field(default=None, max_length=255)
    editor_name: str | None = Field(default=None, max_length=255)
    publication_year: str | None = Field(default=None, max_length=255)
    publication_place: str | None = Field(default=None, max_length=255)
    no_of_pages: int | None = Field(default=None)
    archive_link: str | None = Field(default=None, max_length=255)
    beginning_line: str | None = Field(default=None, max_length=255)
    ending_line: str | None = Field(default=None, max_length=255)
    colophon: str | None = Field(default=None, max_length=255)

    manuscripts: list["Manuscript"] = Relationship(back_populates="book")


class Manuscript(EntityBase, table=True):
    accession_number: str = Field(unique=True, index=True, max_length=255)
    name: str = Field(index=True, max_length=255)
    indic_name: str = Field(index=True, max_length=255)
    diacritical_name: str = Field(index=True, max_length=255)

    language_id: Optional[int] = Field(default=None, foreign_key="language.id")
    language: Optional[Language] = Relationship(back_populates="manuscripts")

    script_id: Optional[int] = Field(default=None, foreign_key="script.id")
    script: Optional[Script] = Relationship(back_populates="manuscripts")

    category_id: Optional[int] = Field(default=None, foreign_key="category.id")
    category: Optional[Category] = Relationship(back_populates="manuscripts")

    type_id: Optional[int] = Field(default=None, foreign_key="type.id")
    type: Optional[Type] = Relationship(back_populates="manuscripts")

    # tags: list[Tag] = Relationship(back_populates="manuscripts", sa_relationship_kwargs={"cascade": "all, delete-orphan"})
    tags: list[Tag] = Relationship(
        back_populates="manuscripts", link_model=ManuscriptTagLink
    )

    subject_id: Optional[int] = Field(default=None, foreign_key="subject.id")
    subject: Optional[Subject] = Relationship(back_populates="manuscripts")
    summary: str | None = Field(default=None, max_length=2000)
    toc: str | None = Field(default=None, max_length=2000)
    date_of_composition: str | None = Field(default=None, max_length=255)
    source: str | None = Field(default=None, max_length=255)
    pg_in_source: str | None = Field(default=None, max_length=255)
    manuscript_code: str | None = Field(default=None, max_length=255)
    is_complete: bool = False
    published: bool = False
    additional_info: list["MSAdditionalInfo"] = Relationship(
        back_populates="manuscript",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
        },
    )
    no_of_folios: str | None = Field(default=None)
    book_id: Optional[int] = Field(default=None, nullable=True, foreign_key="book.id")
    book: Optional["Book"] = Relationship(back_populates="manuscripts")


class MSAdditionalInfo(EntityBase, table=True):
    manuscript_id: Optional[int] = Field(default=None, foreign_key="manuscript.id")
    manuscript: Optional[Manuscript] = Relationship(back_populates="additional_info")

    # no_of_folios: str | None = Field(default=None)
    subject_contribution: str | None = Field(default=None, max_length=5000)
    work_uniqueness: str | None = Field(default=None, max_length=5000)
    author_name: str | None = Field(default=None, max_length=255)
    author_indic_name: str | None = Field(default=None, max_length=255)
    author_diacritical_name: str | None = Field(default=None, max_length=255)
    # date_of_composition: str | None = Field(default=None, max_length=255)
    # source: str | None = Field(default=None, max_length=255)
    # pg_in_source: str | None = Field(default=None, max_length=255)
    # published_title: str | None = Field(default=None, max_length=255)
    # translator_name: str | None = Field(default=None, max_length=255)
    # publisher_name: str | None = Field(default=None, max_length=255)
    # editor_name: str | None = Field(default=None, max_length=255)
    # publication_year: str | None = Field(default=None, max_length=255)
    # publication_place: str | None = Field(default=None, max_length=255)
    # no_of_pages: int | None = Field(default=None)
    # archive_link: str | None = Field(default=None, max_length=255)
    # beginning_line: str | None = Field(default=None, max_length=255)
    # ending_line: str | None = Field(default=None, max_length=255)
    # colophon: str | None = Field(default=None, max_length=255)
    notes: str | None = Field(default=None, max_length=1000)


# Generic message
class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: str | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=128)


# PUBLIC RESPONSE SCHEMAS


class BranchOnlyPublic(SQLModel):
    id: int
    short_name: str
    name: str
    indic_name: str
    active: bool

    model_config = {"from_attributes": True}


class DisciplineOnlyPublic(SQLModel):
    id: int
    short_name: str
    name: str
    indic_name: str
    active: bool

    branch: Optional["BranchOnlyPublic"] = None

    model_config = {"from_attributes": True}


class SubjectPublic(SQLModel):
    id: int
    short_name: str
    name: str
    indic_name: str
    active: bool

    # discipline: Optional["DisciplineOnlyPublic"] = None

    model_config = {"from_attributes": True}


class DisciplinePublic(SQLModel):
    id: int
    short_name: str
    name: str
    indic_name: str
    active: bool
    subjects: list[SubjectPublic] = []

    model_config = {"from_attributes": True}


class BranchPublic(SQLModel):
    id: int
    short_name: str
    name: str
    indic_name: str
    active: bool
    disciplines: list[DisciplinePublic] = []

    model_config = {"from_attributes": True}


# MANUSCRIPT PUBLIC SCHEMAS


class TagPublic(SQLModel):
    id: int
    short_name: str
    name: str

    model_config = {"from_attributes": True}


class LanguagePublic(SQLModel):
    id: int
    short_name: str
    name: str

    model_config = {"from_attributes": True}


class ScriptPublic(SQLModel):
    id: int
    short_name: str
    name: str

    model_config = {"from_attributes": True}


class CategoryPublic(SQLModel):
    id: int
    short_name: str
    name: str

    model_config = {"from_attributes": True}


class TypePublic(SQLModel):
    id: int
    short_name: str
    name: str

    model_config = {"from_attributes": True}


class BookPublic(SQLModel):
    id: int
    published_title: str | None = None
    translator_name: str | None = None
    publisher_name: str | None = None
    editor_name: str | None = None
    publication_year: str | None = None
    publication_place: str | None = None
    no_of_pages: int | None = None
    archive_link: str | None = None
    beginning_line: str | None = None
    ending_line: str | None = None
    colophon: str | None = None

    original_title: str | None = None
    author_name: str | None = None
    manuscript_id: int | None = None

    model_config = {"from_attributes": True}


class AdditionalInfoPublic(SQLModel):
    id: int
    # no_of_folios: str | None = None
    subject_contribution: str | None = None
    work_uniqueness: str | None = None
    author_name: str | None = None
    author_indic_name: str | None = None
    author_diacritical_name: str | None = None
    # date_of_composition: str | None = None
    # source: str | None = None
    # pg_in_source: str | None = None
    # published_title: str | None = None
    # translator_name: str | None = None
    # publisher_name: str | None = None
    # editor_name: str | None = None
    # publication_year: str | None = None
    # publication_place: str | None = None
    # no_of_pages: int | None = None
    # archive_link: str | None = None
    # beginning_line: str | None = None
    # ending_line: str | None = None
    # colophon: str | None = None
    notes: str | None = None

    model_config = {"from_attributes": True}


class BranchMini(SQLModel):
    id: int
    name: str
    model_config = {"from_attributes": True}


class DisciplineMini(SQLModel):
    id: int
    name: str
    branch: BranchMini | None = None
    model_config = {"from_attributes": True}


class SubjectWithClassification(SQLModel):
    id: int
    name: str
    discipline: DisciplineMini | None = None
    model_config = {"from_attributes": True}


class ManuscriptPublic(SQLModel):
    id: int
    accession_number: str | None = None
    name: str
    indic_name: str
    diacritical_name: str
    summary: str | None = None
    toc: str | None = None
    manuscript_code: str | None = None
    is_complete: bool
    published: bool

    no_of_folios: str | None = None
    date_of_composition: str | None = None
    source: str | None = None
    pg_in_source: str | None = None

    language: LanguagePublic | None = None
    script: ScriptPublic | None = None
    category: CategoryPublic | None = None
    type: TypePublic | None = None
    subject: SubjectWithClassification | None = None
    tags: list[TagPublic] = []
    additional_info: list[AdditionalInfoPublic] = []
    book: BookPublic | None = None

    model_config = {"from_attributes": True}


SubjectPublic.model_rebuild()
DisciplineOnlyPublic.model_rebuild()


SubjectWithClassification.model_rebuild()
DisciplineMini.model_rebuild()
