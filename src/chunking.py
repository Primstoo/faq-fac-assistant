"""
Découpage du texte brut en chunks avec chevauchement, pour la recherche
par similarité (un document entier est trop grand pour être comparé d'un bloc).
"""
def chunk_text(text, chunk_size=1000, overlap=200):
    """
    Découpe le texte en morceaux de taille chunk_size avec un chevauchement overlap.
    """
    chunks = []
    start = 0
    text_length = len(text)
    
    while start < text_length:
        end = min(start + chunk_size, text_length)
        chunk = text[start:end]
        chunks.append(chunk)
        
        # Avance le début pour le prochain chunk en tenant compte du chevauchement
        start += chunk_size - overlap
    
    return chunks
