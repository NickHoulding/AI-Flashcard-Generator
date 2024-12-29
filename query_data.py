import os
import re

from get_embedding_function import get_embedding_function
from langchain.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
from langchain_chroma import Chroma

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

# Augments user query wit RAG for AI model.
def query_rag(query_text: str):
    """
    Queries the databse for relevant knowledge, sends it 
    to the AI with the user's query, then sanitizes and 
    returns the html formatted response and sources.

    Args:
        query_text (str): Query text to search the database.
    Returns:
        tuple: A tuple containing two HTML formatted strings:
            - response_html (str): The AI-generated response,
            formatted in HTML.
            - sources_html (str): The sources used by the AI
            to generate the response, formatted in HTML.
    """
    
    # Get a reference to the database.
    db = Chroma(
        persist_directory=r"chroma_db",
        embedding_function=get_embedding_function(),
    )

    # Get and format relevant context from database.
    results = db.similarity_search(query_text, k=5)
    context_text = "\n\n---\n\n".join(
        [
            doc.page_content 
            for doc in results
        ]
    )
    prompt_template = ChatPromptTemplate.from_template(
        PROMPT_TEMPLATE
    )
    prompt = prompt_template.format(
        context=context_text,
        question=query_text
    )

    # Get AI response: Sanitize format and styling.
    model = OllamaLLM(model="llama3.2")
    response_html = model.invoke(prompt)

    # Remove the first h1 tag and all unwanted styling.
    if response_html.startswith("<h1"):
        response_html = re.sub(
            r"<h1.*?>.*?</h1>", 
            "", 
            response_html, 
            count=1
        )
    response_html = re.sub(
        r"<style.*?>.*?</style>", 
        "", 
        response_html, 
        flags=re.DOTALL
    )

    # Get sources: Sanitize format and styling.
    sources = list(
        set([
            f"{os.path.basename(doc.metadata.get('source'))}:"
            + f"{doc.metadata.get('page')}"
            for doc in results
        ])
    )
    sources_html = (
        "<h3 class='sources-title'>Sources</h3>"
        "<div class='source-container'>"
        + "".join(
            [
                f"<p class='source'>{source}</p>"
                for source in sources
            ]
        )
        + "</div>"
    )

    # Return response and source html formatted strings.
    return response_html, sources_html