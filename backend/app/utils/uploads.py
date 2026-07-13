import os
from typing import Iterable

from fastapi import HTTPException, UploadFile

ALLOWED_DOCUMENT_EXTENSIONS = (".pdf", ".jpg", ".jpeg", ".png")
MAX_DOCUMENT_SIZE_BYTES = 10 * 1024 * 1024

ALLOWED_SHARED_FILE_EXTENSIONS = (
    ".pdf", ".jpg", ".jpeg", ".png",
    ".xls", ".xlsx", ".csv",
    ".doc", ".docx",
    ".zip",
)
MAX_SHARED_FILE_SIZE_BYTES = 25 * 1024 * 1024


def _human_size(num_bytes: int) -> str:
    return f"{num_bytes / (1024 * 1024):.0f} MB"


def validate_upload(
    file: UploadFile,
    allowed_extensions: Iterable[str] = ALLOWED_DOCUMENT_EXTENSIONS,
    max_size_bytes: int = MAX_DOCUMENT_SIZE_BYTES,
) -> bytes:
    if not file or not file.filename:
        raise HTTPException(status_code=400, detail="No file was uploaded")

    allowed = tuple(e.lower() for e in allowed_extensions)
    extension = os.path.splitext(file.filename)[1].lower()
    if extension not in allowed:
        pretty = ", ".join(e.lstrip(".").upper() for e in allowed)
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file format '{extension or 'unknown'}'. Allowed formats: {pretty}."
        )

    contents = file.file.read()
    file.file.seek(0)

    if len(contents) == 0:
        raise HTTPException(status_code=400, detail="The uploaded file is empty")
    if len(contents) > max_size_bytes:
        raise HTTPException(
            status_code=400,
            detail=f"File is too large ({_human_size(len(contents))}). Maximum allowed size is {_human_size(max_size_bytes)}."
        )

    return contents
