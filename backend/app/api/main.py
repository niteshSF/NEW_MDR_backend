from fastapi import APIRouter

from app.api.routes import (
    login,
    private,
    users,
    utils,
    branches,
    disciplines,
    subjects,
    languages,
    scripts,
    categories,
    types,
    tags,
    manuscripts,
    viewDocument,
)

from app.core.config import settings

api_router = APIRouter()

# Auth & Users
api_router.include_router(login.router)
api_router.include_router(users.router)
api_router.include_router(utils.router)

# New Demo APIs
api_router.include_router(branches.router)
api_router.include_router(disciplines.router)
api_router.include_router(subjects.router)
api_router.include_router(languages.router)
api_router.include_router(scripts.router)
api_router.include_router(categories.router)
api_router.include_router(types.router)
api_router.include_router(tags.router)
api_router.include_router(manuscripts.router)
api_router.include_router(viewDocument.router, tags=["viewDocument"])

# Private routes only in local
if settings.ENVIRONMENT == "local":
    api_router.include_router(private.router)
