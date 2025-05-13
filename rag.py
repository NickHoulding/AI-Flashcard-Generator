import concurrent.futures
import tempfile
import pypdf
import os
import re
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.prompts import ChatPromptTemplate
from langchain.schema.document import Document
from embeddings import get_embedding_function
from config import get_absolute_path
from langchain_chroma import Chroma

PROMPT_TEMPLATE = """
Create a comprehensive set of study flashcards based only on the following context:
{context}

---
Generate a comprehensive set of study flashcards from the following prompt:
{prompt}
"""

def get_db(
    ) -> Chroma:
    """
    Gets a reference to the Chroma database.

    Args:
        None
    
    Returns:
        Chroma: A reference to the Chroma database.
    
    Raises:
        ValueError: If the DB_DIR environment variable is not set.
    """
    return Chroma(
        persist_directory=get_absolute_path("DB_DIR"), 
        embedding_function=get_embedding_function(),
    )

def split_documents(
        documents: list[Document]
    ) -> list[Document]:
    """
    Splits the documents into chunks.

    Args:
        documents (list[Document]): Documents to split.
    
    Returns:
        list[Document]: The chunks of the documents.
    
    Raises:
        None
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=80,
        length_function=len,
        is_separator_regex=False,
    )
    
    return text_splitter.split_documents(documents)

def create_chunk_ids(
        chunks: list[Document], 
        db: Chroma
    ) -> None:
    """
    Creates new chunk IDs for the chunks.

    Args:
        chunks (list[Document]): Chunks to create IDs for.
        db (Chroma): The Chroma database.
    
    Returns:
        None
    
    Raises:
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

def get_new_chunks(
        chunks: list[Document], 
        existing_ids: set
    ) -> list[Document]:
    """
    Gets the new chunks to add to the database using efficient filtering.

    Args:
        chunks (list[Document]): The chunks to check.
        existing_ids (set): Existing database IDs.
    
    Returns:
        list[Document]: New chunks for the database.
    
    Raises:
        None
    """
    return [chunk 
        for chunk in chunks 
        if chunk.metadata["id"] not in existing_ids
    ]

def set_chunk_ids(
        new_chunks: list[Document], 
        existing_ids: set
    ) -> list[str]:
    """
    Sets the new IDs for the new chunks.

    Args:
        new_chunks (list[Document]): New chunks to add.
        existing_ids (set): Existing database IDs.
    
    Returns:
        list[str]: The new chunk IDs.
    
    Raises:
        None
    """
    new_chunk_ids = [
        chunk.metadata["id"] 
        for chunk in new_chunks
    ]

    return new_chunk_ids

def add_to_chroma(
        chunks: list[Document]
    ) -> None:
    """
    Inserts the document chunks into the database.

    Args:
        chunks (list[Document]): Chunks to add.
    
    Returns:
        None
    
    Raises:
        None
    """
    db = get_db()
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

def _process_batch(
        batch_start: int, 
        batch_end: int, 
        pdf_reader: pypdf.PdfReader, 
        source_path: str, 
        filename: str, 
        total_pages: int
    ) -> None:
    """
    Helper function to process a single batch of PDF pages.
    
    Args:
        batch_start (int): Starting page index.
        batch_end (int): Ending page index.
        pdf_reader (PdfReader): The PDF reader.
        source_path (str): Path to source file.
        filename (str): Name of the file.
        total_pages (int): Total pages in the PDF.
        
    Returns:
        None
    """
    documents = []
    
    for i in range(batch_start, batch_end):
        text = pdf_reader.pages[i].extract_text()
        
        if text.strip():
            metadata = {
                "source": source_path,
                "page": i,
                "total_pages": total_pages
            }
            documents.append(
                Document(
                    page_content=text, 
                    metadata=metadata
                )
            )
    
    if documents:
        chunks = split_documents(documents)
        add_to_chroma(chunks)

def process_file(
        file_content: bytes,
        filename: str
    ) -> None:
    """
    Process a single file from memory and add it to the database.
    Uses multithreaded batch processing for improved performance.

    Args:
        file_content (bytes): The content of the file.
        filename (str): The name of the file.
    
    Returns:
        None
    
    Raises:
        None
    """
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(file_content)
        temp_file_path = temp_file.name
    
    try:
        pdf_reader = pypdf.PdfReader(temp_file_path)
        total_pages = len(pdf_reader.pages)
        source_path = os.path.join(get_absolute_path("CACHE_DIR"), filename)
        
        batch_size = 5
        tpe = concurrent.futures.ThreadPoolExecutor(
            max_workers=min(
                os.cpu_count() * 2, 
                8
            )
        )

        with tpe as executor:
            futures = []
            
            for batch_start in range(0, total_pages, batch_size):
                batch_end = min(batch_start + batch_size, total_pages)
                
                futures.append(
                    executor.submit(
                        _process_batch,
                        batch_start,
                        batch_end,
                        pdf_reader,
                        source_path,
                        filename,
                        total_pages
                    )
                )
            
            concurrent.futures.wait(futures)
            
    finally:
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

def del_from_chroma(
        filename: str
    ) -> None:
    """
    Deletes all chunks with a source of filename.

    Args:
        filename (str): Name of the file to delete.
    
    Returns:
        None
    
    Raises:
        ValueError: If the CACHE_DIR environment variable is not set.
    """
    db = get_db()
    file_source = os.path.join(get_absolute_path("CACHE_DIR"), filename)
    
    matching_chunks = db.get(
        where={"source": file_source}
    )
    
    ids = matching_chunks['ids']
    db.delete(ids=ids)

def get_context_prompt(
        query_text: str
    ) -> tuple[str, list[Document]]:
    """
    Appends relevant context to the user query.

    Args:
        query_text (str): The user query.
    
    Returns:
        tuple[str, list[Document]]: The prompt and relevant documents.
    
    Raises:
        None
    """
    db = get_db()
    results = db.similarity_search_with_relevance_scores(
        query_text, 
        k=10
    )
    results = [
        results[i][0] 
        for i in range(len(results)) 
        if results[i][1] > 0.5
    ]

    context_text = "\n\n---\n\n".join([
            doc.page_content 
            for doc in results
    ])
    prompt_template = ChatPromptTemplate.from_template(
        PROMPT_TEMPLATE
    )
    prompt = prompt_template.format(
        context=context_text,
        prompt=query_text
    )

    return prompt, results

def get_file_names(
    ) -> list[str]:
    """
    Gets the names of the files in the database.

    Args:
        None
    
    Returns:
        list[str]: List of filenames.
    
    Raises:
        None
    """
    db = get_db()
    chunks = db.get(include=[])
    
    seen = {}
    for cid in chunks["ids"]:
        filename = os.path.basename(
            re.sub(r':\d+:\d+$', '', cid)
        )
        seen[filename] = True

    return sorted(seen.keys())