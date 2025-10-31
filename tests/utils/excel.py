"""Generate an Excel file suitable for the app's Import Excel page."""
from __future__ import annotations
from openpyxl import Workbook
from pathlib import Path
from typing import Iterable

def make_users_excel(path: Path, rows: Iterable[tuple[str,str,str,str]]) -> Path:
    """Create an Excel file with columns: username, email, first_name, last_name."""
    wb = Workbook()
    ws = wb.active
    ws.append(["username","email","first_name","last_name"])  # header as per template
    for row in rows:
        ws.append(list(row))
    wb.save(path)
    return path
