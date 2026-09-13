import pytest

from src.ingestion import read_document, read_txt


def test_read_txt_returns_file_content(tmp_path):
    fichier = tmp_path / "doc.txt"
    fichier.write_text("Article 1 — Inscription administrative", encoding="utf-8")
    assert read_txt(fichier) == "Article 1 — Inscription administrative"


def test_read_document_dispatches_on_txt_extension(tmp_path):
    fichier = tmp_path / "doc.txt"
    fichier.write_text("contenu", encoding="utf-8")
    assert read_document(fichier) == "contenu"


def test_read_document_rejects_unknown_extension(tmp_path):
    fichier = tmp_path / "doc.docx"
    fichier.write_text("contenu", encoding="utf-8")
    with pytest.raises(ValueError):
        read_document(fichier)
