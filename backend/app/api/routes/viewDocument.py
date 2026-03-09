from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path

router = APIRouter()

# Your real folder path
from pathlib import Path

# Auto-detect backend root directory
BASE_DIR = Path(__file__).resolve()

while BASE_DIR.name != "backend":
    BASE_DIR = BASE_DIR.parent

DOCUMENTS_DIR = BASE_DIR / "scripts" / "documents"


# List PDFs inside manuscript folder
@router.get("/viewDocument/{name}")
def list_files(name: str):
    folder_path = DOCUMENTS_DIR / name

    if not folder_path.exists():
        raise HTTPException(status_code=404, detail="Folder not found")

    files = [
        f.name
        for f in folder_path.iterdir()
        if f.is_file() and f.suffix.lower() in [".pdf", ".jpg", ".jpeg", ".png"]
    ]

    return {"name": name, "files": files}


@router.get("/viewDocument/{name}/{filename}")
def get_pdf(name: str, filename: str):
    file_path = DOCUMENTS_DIR / name / filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(file_path)
