from __future__ import annotations
from pathlib import Path
import fitz

def extract_text(pdf_path: Path, pages: list[int] | None = None) -> PageText:
    """
    Extracts text from a PDF file.

    Args:
        pdf_path (Path): The path to the PDF file.
        pages (list[int] | None): List of page numbers to extract (0-indexed). If None, extract all pages.
    Returns:
        dict[int, str]: A dictionary mapping page numbers (1-indexed) to extracted text.
    """
    doc = fitz.open(pdf_path)
    data: dict[int, str] = {}

    if pages is None:
        page_numbers = range(doc.page_count)
    else:
        page_numbers = pages

    for page_number in page_numbers:
        page = doc.load_page(page_number)
        text = page.get_text("text")  # explicit
        data[page_number + 1] = text.rstrip() + "\n"

    return data

def parse_pages(pages_str: str, num_pages: int) -> list[int]:
    """
    Parses a pages range string into a list of page numbers.

    Args:
        pages_str (str): The pages range string (e.g., "1-3,5,7-9").
        num_pages (int): The total number of pages in the document.
        
    Returns:
        list[int]: A list of page numbers (0-indexed).
    """
    pages: set[int] = set()
    for part in pages_str.split(","):
        if "-" in part:
            start_str, end_str = part.split("-", 1)
            start = int(start_str) - 1
            end = int(end_str) - 1
            pages.update(range(start, end + 1))
        else:
            page = int(part) - 1
            pages.add(page)
    valid_pages = [p for p in pages if 0 <= p < num_pages]
    return sorted(valid_pages)