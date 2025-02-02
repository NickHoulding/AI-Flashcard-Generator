from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.prompts import ChatPromptTemplate
from langchain.schema.document import Document
from embeddings import get_embedding_function
from langchain_chroma import Chroma
from config import get_env_var

PROMPT_TEMPLATE = """
Answer the questions based only on the following context:
{context}

---
Answer the question based on the above context: {question}. 
Respond in strictly valid HTML format only. 
Only use tags including <p>, <ul>, <li>, and header tags.
Ensure your html response is ready to be rendered in a browser.
Always begin your responses with a <h1> tag.
"""

def get_chroma_db() -> Chroma:
    """
    Gets a reference to the Chroma database.

    Args:
        None
    Returns:
        Chroma: A reference to the Chroma database.
    """
    return Chroma(
        persist_directory=get_env_var("DB_PERSIST_DIR"), 
        embedding_function=get_embedding_function(),
    )

def load_documents() -> list[Document]:
    """
    Loads the documents from the tmp directory.

    Args:
        None
    Returns:
        list[Document]: The documents loaded from the directory.
    """
    document_loader = PyPDFDirectoryLoader(
        get_env_var("CACHE_DIR")
    )

    return document_loader.load()

def split_documents(documents: list[Document]) -> list[Document]:
    """
    Splits the documents into chunks.

    Args:
        documents (list[Document]): The documents to split.
    Returns:
        list[Document]: The chunks of the documents.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=80,
        length_function=len,
        is_separator_regex=False,
    )
    
    return text_splitter.split_documents(documents)

def create_chunk_ids(chunks: list[Document], db: Chroma):
    """
    Creates new chunk IDs for the chunks.

    Args:
        chunks (list[Document]): The chunks to create IDs for.
        db (Chroma): The Chroma database.
    Returns:
        None
    """
    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"

        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        last_page_id = current_page_id
        chunk_id = (
            f"{current_page_id}:"
            + f"{current_chunk_index}"
        )
        chunk.metadata["id"] = chunk_id

def get_new_chunks(chunks: list[Document], existing_ids: set) -> list[Document]:
    """
    Gets the new chunks to add to the database.

    Args:
        chunks (list[Document]): The chunks to check.
        existing_ids (set): The existing IDs in the database.
    Returns:
        list[Document]: The new chunks to add to the database.
    """
    new_chunks = []

    for chunk in chunks:
        if chunk.metadata["id"] not in existing_ids:
            new_chunks.append(chunk)
    
    return new_chunks

def set_chunk_ids(new_chunks: list[Document], existing_ids: set) -> list[str]:
    """
    Sets the new IDs for the new chunks.

    Args:
        new_chunks (list[Document]): The new chunks to add.
        existing_ids (set): The existing IDs in the database.
    Returns:
        list[str]: The new chunk IDs.
    """
    new_chunk_ids = [
        chunk.metadata["id"] 
        for chunk in new_chunks
    ]

    return new_chunk_ids

def add_to_chroma(chunks: list[Document]):
    """
    Inserts the document chunks into the database.

    Args:
        chunks (list[Document]): Chunks to insert into the DB.
    Returns:
        None
    """
    db = get_chroma_db()
    create_chunk_ids(chunks, db)
    existing_items = db.get(include=[])
    existing_ids = set(existing_items["ids"])
    new_chunks = get_new_chunks(chunks, existing_ids)
    new_chunk_ids = set_chunk_ids(new_chunks, existing_ids)

    if new_chunks:
        db.add_documents(
            documents=new_chunks, 
            ids=new_chunk_ids
        )

def del_from_chroma(filename: str):
    """
    Deletes all chunks with a source of filename.

    Args:
        filename (str): The name of the file to delete.
    Returns:
        None
    """
    db = get_chroma_db()
    file_source = get_env_var("CACHE_DIR") + "/" + filename
    matching_chunks = db.get(
        where={"source": file_source}
    )
    ids = matching_chunks['ids']
    db.delete(ids=ids)

def update_database():
    """
    Updates the database with the new chunks.

    Args:
        None
    Returns:
        None
    """
    documents = load_documents()
    chunks = split_documents(documents)
    add_to_chroma(chunks)

def get_context_prompt(query_text: str) -> tuple[str, list[Document]]:
    """
    Retreives most relevant context from the database using the user's query.

    Args:
        query_text (str): The query text to search the database.
    Returns:
        tuple[str, list[Document]]: The context prompt and the search results.
    """
    db = get_chroma_db()
    results = db.similarity_search(
        query_text, 
        k=5
    )
    context_text = "\n\n---\n\n".join([
            doc.page_content 
            for doc in results
    ])
    prompt_template = ChatPromptTemplate.from_template(
        PROMPT_TEMPLATE
    )
    prompt = prompt_template.format(
        context=context_text,
        question=query_text
    )

    return prompt, results