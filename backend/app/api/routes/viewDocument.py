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
@router.get("/viewDocument/{accession_number}")
def list_pdfs(accession_number: str):
    folder_path = DOCUMENTS_DIR / accession_number

    if not folder_path.exists():
        raise HTTPException(status_code=404, detail="Folder not found")

    files = [
        f.name
        for f in folder_path.iterdir()
        if f.is_file() and f.suffix.lower() == ".pdf"
    ]

    return {"accession_number": accession_number, "files": files}


# Open / Download specific PDF
@router.get("/viewDocument/{accession_number}/{filename}")
def get_pdf(accession_number: str, filename: str):
    file_path = DOCUMENTS_DIR / accession_number / filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(file_path)
