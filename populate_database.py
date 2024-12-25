import langchain_chroma

from get_embedding_function import get_embedding_function
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema.document import Document

def load_documents():
    document_loader = PyPDFDirectoryLoader(r"data")
    return document_loader.load()

def split_documents(documents: list[Document]):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=80,
        length_function=len,
        is_separator_regex=False,
    )
    return text_splitter.split_documents(documents)

def add_to_chroma(chunks: list[Document]):
    db = langchain_chroma.Chroma(
        persist_directory=r"chroma_db", 
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
        chunk_id = f"{current_page_id}:{current_chunk_index}"
        chunk.metadata["id"] = chunk_id

    existing_items = db.get(include=[])
    existing_ids = set(existing_items["ids"])
    print(f"Number of existing documents in DB: {len(existing_ids)}")

    new_chunks = []
    for chunk in chunks:
        if chunk.metadata["id"] not in existing_ids:
            new_chunks.append(chunk)
    
    print(f"Number of new documents to add: {len(new_chunks)}")
    new_chunk_ids = [chunk.metadata["id"] for chunk in new_chunks]
    print("adding documents")

    if new_chunks:
        db.add_documents(new_chunks, ids=new_chunk_ids)
    else:
        print("No new documents to add")
    
    print("done")

def update_database():
    documents = load_documents()
    chunks = split_documents(documents)
    add_to_chroma(chunks)