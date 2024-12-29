from langchain_ollama import OllamaEmbeddings

# Returns standard embedding function for all modules.
def get_embedding_function():
    embeddings = OllamaEmbeddings(
        model="nomic-embed-text"
    )
    return embeddings