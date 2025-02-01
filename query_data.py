import os
import re

from get_embedding_function import get_embedding_function
from langchain_ollama import OllamaLLM
from langchain_chroma import Chroma
from config import get_env_var
from rag import get_chroma_db, get_context_prompt

def query_ollama(prompt):
    """
    Queries Ollama AI with prompt.

    Args:
        prompt (str): The prompt to query the model.
    Returns:
        html_response (str): The response from the Ollama model.
    """
    model = OllamaLLM(
        model=get_env_var("MODEL_NAME")
    )

    return model.invoke(prompt)

def query_huggingface(prompt):
    # TODO: Implement HF support.

    return ""

def format_response(response_html, results):
    """
    Formats the response from the RAG model.

    Args:
        response_html (str): The HTML response from the RAG model.
    Returns:
        tuple:
            response_html (str): The formatted response.
            sources_html (str): The sources of the information.
    """
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

    return response_html, sources_html

def handle_platform(prompt, platform):
    """
    Delegates the query to the appropriate platform.

    Args:
        prompt (str): The prompt to query the model.
        platform (str): The platform to query.
    Returns:
        response_html (str): The response from the model.
    """
    response_html = ""

    match platform:
        case "ollama":
            response_html = query_ollama(prompt)
        case "huggingface":
            response_html = query_huggingface(prompt)

    return response_html

def query(query_text, platform):
    """
    Queries the databse for relevant knowledge.

    Args:
        query_text (str): Query text to search the database.
        platform (str): The platform to query.
    Returns:
        html_response (str): The response from the RAG model.
        sources_html (str): The sources of the information.
    """
    prompt, results = get_context_prompt(query_text)
    response_html = handle_platform(prompt, platform)
    response = format_response(response_html, results)

    return response