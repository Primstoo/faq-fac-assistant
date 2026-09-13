import pytest

from src.chunking import chunk_text


def test_short_text_gives_one_chunk():
    texte = "Phrase courte."
    assert chunk_text(texte, chunk_size=1000, overlap=200) == [texte]


def test_chunks_never_exceed_chunk_size():
    texte = "a" * 2500
    chunks = chunk_text(texte, chunk_size=1000, overlap=200)
    assert all(len(chunk) <= 1000 for chunk in chunks)


def test_consecutive_chunks_overlap():
    texte = "".join(str(i % 10) for i in range(2500))
    chunks = chunk_text(texte, chunk_size=1000, overlap=200)
    # La fin d'un chunk doit se retrouver au début du suivant.
    assert chunks[0][-200:] == chunks[1][:200]


def test_no_text_is_lost():
    texte = "".join(str(i % 10) for i in range(2500))
    chunks = chunk_text(texte, chunk_size=1000, overlap=200)
    reconstruit = chunks[0] + "".join(chunk[200:] for chunk in chunks[1:])
    assert reconstruit == texte


def test_empty_text_gives_no_chunk():
    assert chunk_text("", chunk_size=1000, overlap=200) == []


def test_overlap_greater_or_equal_to_chunk_size_is_rejected():
    # Sans ce garde-fou, start n'avance plus et la boucle tourne indéfiniment.
    with pytest.raises(ValueError):
        chunk_text("texte quelconque", chunk_size=100, overlap=100)
