from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from get_embedding_function import get_embedding_function
from langchain.schema.document import Document
from langchain_chroma import Chroma
from config import get_env_var

# Loads PDF files in the temp data directory.
def load_documents(file_paths):
    docs = []

    for file_path in file_paths:
        document_loader = PyPDFLoader(
            file_path=file_path,
        )
        docs.append(document_loader.load())
    
    return docs

# Splits the documents into chunks.
def split_documents(documents: list[Document]):
    '''
    Splits the documents into chunks

    Args:
        documents (list[Document]): Documents to split.
    Returns:
        list[Document]: Chunks of the documents.
    '''
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=80,
        length_function=len,
        is_separator_regex=False,
    )

    chunks = []
    for document in documents:
        chunks.extend(
            text_splitter.split_documents(document)
        )

    return chunks

# Adds the chunks to the database.
def add_to_chroma(chunks: list[Document]):
    '''
    Inserts the document chunks into the database.

    Args:
        chunks (list[Document]): Chunks to insert into the DB.
    Returns:
        None
    '''

    db = Chroma(
        persist_directory=get_env_var("DB_PERSIST_DIR"), 
        embedding_function=get_embedding_function(),
    )

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

    existing_items = db.get(include=[])
    existing_ids = set(existing_items["ids"])

    print(f"Number of existing documents in DB: {len(existing_ids)}")

    new_chunks = []
    for chunk in chunks:
        if chunk.metadata["id"] not in existing_ids:
            new_chunks.append(chunk)
    
    print(f"Number of new documents to add: {len(new_chunks)}")

    new_chunk_ids = ([
        chunk.metadata["id"] 
        for chunk in new_chunks
    ])

    print("adding documents...")

    if new_chunks:
        db.add_documents(
            documents=new_chunks, 
            ids=new_chunk_ids
        )
    else:
        print("No new documents to add")
    
    print("done")

# Updates the database with the new chunks.
def update_database(file_paths):
    documents = load_documents(file_paths)
    chunks = split_documents(documents)
    add_to_chroma(chunks)