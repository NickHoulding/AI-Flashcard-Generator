from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from get_embedding_function import get_embedding_function
from langchain.schema.document import Document
from langchain_chroma import Chroma
from config import get_env_var

# Loads PDF files in the temp data directory.
def load_documents():
    document_loader = PyPDFDirectoryLoader(
        get_env_var("TEMP_DATA_DIR")
    )
    return document_loader.load()

# Splits the documents into chunks.
def split_documents(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=80,
        length_function=len,
        is_separator_regex=False,
    )
    # Return a list of chunks (list[Document]).
    return text_splitter.split_documents(documents)

# Adds the chunks to the database.
def add_to_chroma(chunks: list[Document]):
    '''
    Inserts the document chunks into the database.

    Args:
        chunks (list[Document]): Chunks to insert into the DB.
    Returns:
        None
    '''

    # Get a reference to the database.
    db = Chroma(
        persist_directory=get_env_var("DB_PERSIST_DIR"), 
        embedding_function=get_embedding_function(),
    )

    last_page_id = None
    current_chunk_index = 0

    # Assign unique IDs to each chunk.
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

    # Check for existing chunks in the DB.
    existing_items = db.get(include=[])
    existing_ids = set(existing_items["ids"])

    print(f"Number of existing documents in DB: {len(existing_ids)}")

    # Gather new chunks to add.
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

    # Add the new chunks to the database.
    if new_chunks:
        db.add_documents(
            documents=new_chunks, 
            ids=new_chunk_ids
        )
    else:
        print("No new documents to add")
    
    print("done")

# Updates the database with the new chunks.
def update_database():
    documents = load_documents()
    chunks = split_documents(documents)
    add_to_chroma(chunks)