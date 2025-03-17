import torch
import os
import re
from transformers import AutoTokenizer, AutoModelForCausalLM
from rag import get_chroma_db, get_context_prompt
from embeddings import get_embedding_function
from langchain_ollama import OllamaLLM
from langchain_chroma import Chroma
from config import get_env_var

def initialize_hf_model(
    ) -> tuple[AutoModelForCausalLM, AutoTokenizer]:
    """
    Initializes the Hugging Face model and tokenizer.

    Args:
        None
    
    Returns:
        tuple[AutoModelForCausalLM, AutoTokenizer]: The model and tokenizer.
    
    Raises:
        None
    """
    if torch.cuda.is_available():
        device = "cuda"
    else:
        device = "cpu"

    tokenizer = AutoTokenizer.from_pretrained(
        get_env_var('HF_MODEL_NAME'),
        cache_dir=get_env_var('HF_CACHE_DIR')
    )
    model = AutoModelForCausalLM.from_pretrained(
        get_env_var('HF_MODEL_NAME'),
        cache_dir=get_env_var('HF_CACHE_DIR')
    )
    model.to(get_env_var('DEVICE'))

    return model, tokenizer

# HF model initialized at runtime.
if get_env_var('PLATFORM') == "hf":
    model, tokenizer = initialize_hf_model()

def query_huggingface(
        prompt: str
    ) -> tuple[str, list[str]]:
    """
    Queries the HF AI model with the user's prompt.

    Args:
        prompt (str): The prompt to query the model.
    
    Returns:
        tuple[str, list[str]]: AI response and sources.
    
    Raises:
        None
    """
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    input_ids = tokenizer.encode(
        prompt, 
        return_tensors="pt"
    ).to(get_env_var('DEVICE'))

    attention_mask = input_ids.ne(
        tokenizer.pad_token_id
    ).to(get_env_var('DEVICE'))

    output = model.generate(
        input_ids=input_ids,
        attention_mask=attention_mask,
        max_length=int(get_env_var('MX_LEN')),
        temperature=0.7,
        pad_token_id=tokenizer.pad_token_id,
        do_sample=True,
        top_p=0.9,
        no_repeat_ngram_size=2,
    )

    response = tokenizer.decode(
        output[0], 
        skip_special_tokens=True
    )

    return response

def query_ollama(
        prompt: str
    ) -> str:
    """
    Queries the Ollama model with the user's prompt.

    Args:
        prompt (str): The prompt to query the model.
    
    Returns:
        html_response (str): Ollama AI response.
    
    Raises:
        None
    """
    model = OllamaLLM(
        model=get_env_var("MODEL_NAME")
    )

    return model.invoke(prompt)

def format_response(
        response_html: str, 
        results: list
    ) -> tuple[str, str]:
    """
    Formats the AI model's response.

    Args:
        response_html (str): The HTML AI response.
        results (list): The results from the database.
    
    Returns:
        tuple[str, str]: Formatted response and sources.
    
    Raises:
        None
    """
    if response_html.startswith("<h1"):
        response_html = re.sub(
            r"<h1.*?.*?</h1>", 
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

    sources = set()
    for doc in results:
        source = doc.metadata.get("source")

        if source not in sources:
            sources.add(
                os.path.basename(source)
            )

    sources_html = (
        "<div class='source-container'>"
        + "".join(
            [
                f"<p class='source'>{source}</p>"
                for source in sources
            ]
        )
        + "</div>"
    )
    if len(sources) > 0:
        sources_html = (
            "<h3 class='sources-title'>Sources</h3>"
            + sources_html
        )

    response_html = re.sub(
        r"<think>.*?</think>",
        "", 
        response_html, 
        flags=re.DOTALL
    )

    return response_html, sources_html

def handle_platform(
        prompt: str
    ) -> str:
    """
    Delegates user queries to the appropriate platform.

    Args:
        prompt (str): The prompt to query the model.
    
    Returns:
        response_html (str): AI response.
    
    Raises:
        None
    """
    response_html = ""

    match get_env_var("PLATFORM"):
        case "ol":
            response_html = query_ollama(prompt)
        case "hf":
            response_html = query_huggingface(prompt)

    return response_html

def query(
        query_text: str
    ) -> tuple[str, str]:
    """
    Handles database retrieval and AI queries.

    Args:
        query_text (str): Database query text.
    
    Returns:
        tuple[str, str]: AI response and sources.
    
    Raises:
        None
    """
    prompt, results = get_context_prompt(query_text)
    response_html = handle_platform(prompt)
    response = format_response(response_html, results)

    return response