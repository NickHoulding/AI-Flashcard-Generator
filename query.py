import torch

from transformers import AutoTokenizer, AutoModelForCausalLM
from config import get_env_var

device = "cuda" if torch.cuda.is_available() else "cpu"

tokenizer = AutoTokenizer.from_pretrained(
    get_env_var('HF_MODEL_NAME'),
    cache_dir=get_env_var('HF_CACHE_DIR')
)
model = AutoModelForCausalLM.from_pretrained(
    get_env_var('HF_MODEL_NAME'),
    cache_dir=get_env_var('HF_CACHE_DIR')
)
model.to(get_env_var('DEVICE'))

def query(message):
    """
    Queries the AI model with the user message.

    Args:
        message (str): The user query for the AI model.
    Returns:
        tuple[str, list[str]]: The AI response and sources used.
    """
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    input_ids = tokenizer.encode(
        message, 
        return_tensors="pt"
    ).to(get_env_var('DEVICE'))
    attention_mask = input_ids.ne(
        tokenizer.pad_token_id
    ).to(get_env_var('DEVICE'))

    output = model.generate(
        input_ids=input_ids,
        attention_mask=attention_mask,
        max_length=500,
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

    if response.startswith(message):
        response = response[len(message) + 1:].strip()

    return response, None # Temp dummy source return value.