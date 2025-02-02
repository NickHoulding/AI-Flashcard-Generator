from langchain_ollama import OllamaEmbeddings

def get_embedding_function() -> OllamaEmbeddings:
    """
    Gets the standard embedding function for all modules.

    Args:
        None
    Returns:
        OllamaEmbeddings: Embedding function for all modules.
    """
    embeddings = OllamaEmbeddings(
        model="nomic-embed-text"
    )
    
    return embeddings