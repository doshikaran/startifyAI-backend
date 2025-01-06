from PyPDF2 import PdfReader
from typing import List

def extract_text_from_pdf(file_path: str) -> List[str]:
    """
    Extract text from a PDF and split it into chunks.
    """
    reader = PdfReader(file_path)
    text_chunks = []
    for page in reader.pages:
        if page.extract_text():
            text_chunks.append(page.extract_text())
    return text_chunks
