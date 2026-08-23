"""
Lecture des documents sources (.txt, .pdf) et extraction de leur texte brut.
"""

from pathlib import Path
from pypdf import PdfReader
def read_pdf(path):
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def read_txt(path):
    with open(path, "r", encoding="utf-8") as file:
        return file.read()

def read_document(path):
    extension = Path(path).suffix.lower()
    if extension == ".pdf":
        return read_pdf(path)
    if extension == ".txt":
        return read_txt(path)
    raise ValueError(f"Unsupported file extension: {extension}")

if __name__ == "__main__":
    texte = read_pdf("data/raw/exemple.pdf")
    print(texte)
