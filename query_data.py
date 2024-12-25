import langchain_chroma
import os

from get_embedding_function import get_embedding_function
from langchain_chroma import Chroma
from langchain_ollama import OllamaLLM
from langchain.prompts import ChatPromptTemplate

PROMPT_TEMPLATE = """
Answer the questions based only on the following context:
{context}

---
Answer the question based on the above context: {question}
"""

def query_rag(query_text: str):
    db = langchain_chroma.Chroma(
        persist_directory=r"chroma_db", 
        embedding_function=get_embedding_function(),
    )

    results = db.similarity_search(query_text, k=5)
    context_text = "\n\n---\n\n".join([doc.page_content for doc in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)

    model = OllamaLLM(model="llama3.2")
    response_text = model.invoke(prompt)
    sources = list(set([f"{os.path.basename(doc.metadata.get('source', 'Unknown'))}:{doc.metadata.get('page', 'Unknown')}" for doc in results]))
    print(response_text)
    print(sources)

    return response_text, sources