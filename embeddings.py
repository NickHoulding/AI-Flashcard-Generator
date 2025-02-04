from langchain_ollama import OllamaEmbeddings

def get_embedding_function() -> OllamaEmbeddings:
    """
    Gets the standard embedding function.

    Args:
        None
    Returns:
        OllamaEmbeddings: The embedding function.
    """
    embeddings = OllamaEmbeddings(
        model="nomic-embed-text"
    )
    
    return embeddings