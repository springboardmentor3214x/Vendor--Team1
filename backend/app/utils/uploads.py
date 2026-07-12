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


def _pending_uploads_rows(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
        })
    return rows


def _pending_uploads_totals(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals


def _pending_uploads_rows_2(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
        })
    return rows
