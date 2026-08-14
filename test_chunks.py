from src.ingestion import read_txt
from src.chunking import chunk_text

texte = read_txt("data/raw/exemple.txt")
chunks = chunk_text(texte)
print(f"Nombre de chunks : {len(chunks)}")
print("--- Chunk 0 ---")
print(chunks[0])
